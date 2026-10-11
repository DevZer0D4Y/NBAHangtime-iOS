import Foundation
import Metal

struct Params {
    var sourceSize: SIMD2<Float>
    var outputSize: SIMD2<Float>
    var frame: Float
    var mode: Int32
}
@main
struct CRTTests {
static func main() throws {
guard let gpu = MTLCreateSystemDefaultDevice(), let queue = gpu.makeCommandQueue() else {
    fatalError("Metal GPU required for CRT regression")
}
let library = try gpu.makeLibrary(source: NewPixieShader.source, options: nil)
let descriptor = MTLRenderPipelineDescriptor()
descriptor.vertexFunction = library.makeFunction(name: "crtVertex")
descriptor.fragmentFunction = library.makeFunction(name: "crtFragment")
descriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
let pipeline = try gpu.makeRenderPipelineState(descriptor: descriptor)
func texture(_ w: Int, _ h: Int, _ format: MTLPixelFormat) -> MTLTexture {
    let d = MTLTextureDescriptor.texture2DDescriptor(pixelFormat: format, width: w, height: h, mipmapped: false)
    d.storageMode = .shared; d.usage = [.shaderRead, .renderTarget]
    return gpu.makeTexture(descriptor: d)!
}
for w in [400, 512, 400] {
    let h = 254
    let input = texture(w, h, .rgba8Unorm)
    var bytes = [UInt8](repeating: 0, count: w*h*4)
    for y in 0..<h { for x in 0..<w {
        let i = (y*w+x)*4
        bytes[i] = y<h/2 ? 220 : 20; bytes[i+1] = 60
        bytes[i+2] = y<h/2 ? 20 : 220; bytes[i+3] = 255
    } }
    bytes.withUnsafeBytes { input.replace(region: MTLRegionMake2D(0,0,w,h), mipmapLevel: 0,
        withBytes: $0.baseAddress!, bytesPerRow: w*4) }
    let feedback = texture(w, h, .bgra8Unorm), accumulated = texture(w, h, .bgra8Unorm)
    let horizontal = texture(w, h, .bgra8Unorm), blur = texture(w, h, .bgra8Unorm)
    let output = texture(640, 480, .bgra8Unorm)
    func pass(_ c: MTLCommandBuffer, _ target: MTLTexture, _ source: MTLTexture, _ previous: MTLTexture, _ blurred: MTLTexture, _ mode: Int32) {
        let d = MTLRenderPassDescriptor()
        d.colorAttachments[0].texture = target; d.colorAttachments[0].loadAction = .clear
        d.colorAttachments[0].storeAction = .store
        let e = c.makeRenderCommandEncoder(descriptor: d)!
        e.setRenderPipelineState(pipeline)
        e.setFragmentTexture(source,index: 0); e.setFragmentTexture(previous,index: 1)
        e.setFragmentTexture(blurred,index: 2)
        var p = Params(sourceSize: SIMD2(Float(w),Float(h)),
            outputSize: SIMD2(Float(target.width),Float(target.height)),frame: 1,mode: mode)
        e.setFragmentBytes(&p,length: MemoryLayout<Params>.stride,index: 0)
        e.drawPrimitives(type: .triangle,vertexStart: 0,vertexCount: 3);e.endEncoding()
    }
    let clear = queue.makeCommandBuffer()!
    let d = MTLRenderPassDescriptor(); d.colorAttachments[0].texture = feedback
    d.colorAttachments[0].loadAction = .clear; d.colorAttachments[0].storeAction = .store
    clear.makeRenderCommandEncoder(descriptor: d)!.endEncoding();clear.commit();clear.waitUntilCompleted()
    for enabled in [true,false,true,false] {
        let c = queue.makeCommandBuffer()!
        if enabled {
            pass(c,accumulated,input,feedback,input,1)
            pass(c,horizontal,accumulated,input,input,2)
            pass(c,blur,horizontal,input,input,3)
        }
        pass(c,output,enabled ? accumulated : input,input,enabled ? blur : input,enabled ? 4 : 0)
        c.commit();c.waitUntilCompleted();precondition(c.status == .completed,"GPU command failed")
        var result = [UInt8](repeating: 0,count: 640*480*4)
        result.withUnsafeMutableBytes { output.getBytes($0.baseAddress!, bytesPerRow: 640*4,
            from: MTLRegionMake2D(0,0,640,480),mipmapLevel: 0) }
        let upper = (120*640+320)*4,lower = (360*640+320)*4
        precondition(result[upper+2]>result[upper] && result[lower]>result[lower+2],"Image orientation changed")
        if !enabled {
            precondition(result[upper+2]==220 && result[upper]==20 && result[lower]==220 && result[lower+2]==20)
        }
    }
}
print("Metal CRT: shader compilation, four passes, image orientation, on/off and 400/512 sizes passed.")

}
}
