import UIKit

/// Keep the original bitmap display when CRT is off, with an optional Metal display.
final class GameScreenView: UIView {
    private let bitmap = UIImageView()
    private var gpu: CRTView?
    private var attemptedGPU = false
    private var pixels = Data()
    private var width = 0, height = 0
    private var frameNumber: Float = 0
    var onUnavailable: (() -> Void)?
    var smooth = false {
        didSet {
            let filter: CALayerContentsFilter = smooth ? .linear : .nearest
            bitmap.layer.magnificationFilter = filter
            bitmap.layer.minificationFilter = filter
        }
    }
    var crt = false {
        didSet {
            guard crt != oldValue else { return }
            if crt && !attemptedGPU {
                attemptedGPU = true
                do {
                    let display = try CRTView(native: true)
                    gpu = display; addSubview(display); display.frame = bounds
                } catch {
                    NSLog("CRT display unavailable: %@", error.localizedDescription)
                    onUnavailable?()
                }
            }
            gpu?.crt = crt
            gpu?.isHidden = !crt
            bitmap.isHidden = crt && gpu != nil
            redraw()
        }
    }
    override init(frame: CGRect) {
        super.init(frame: frame)
        backgroundColor = .black
        bitmap.contentMode = .scaleToFill
        bitmap.layer.magnificationFilter = .nearest
        bitmap.layer.minificationFilter = .nearest
        addSubview(bitmap)
        isUserInteractionEnabled = false
    }
    convenience init() { self.init(frame: .zero) }
    required init?(coder: NSCoder) { fatalError("init(coder:) unsupported") }
    override func layoutSubviews() {
        super.layoutSubviews()
        bitmap.frame = bounds; gpu?.frame = bounds
        if crt { gpu?.draw() }
    }
    func upload(_ bytes: UnsafePointer<UInt8>, width: Int, height: Int) {
        guard width > 0, height > 0 else { return }
        self.width = width; self.height = height
        pixels = Data(bytes: bytes, count: width * height * 4)
        frameNumber += 1
        redraw()
    }
    private func redraw() {
        guard width > 0, height > 0 else { return }
        if crt, let gpu {
            pixels.withUnsafeBytes { buffer in
                guard let bytes = buffer.baseAddress?.assumingMemoryBound(to: UInt8.self) else { return }
                gpu.upload(bytes, width: width, height: height, frameNumber: frameNumber)
            }
            gpu.draw()
        } else if let provider = CGDataProvider(data: pixels as CFData),
                  let image = CGImage(width: width, height: height, bitsPerComponent: 8,
                    bitsPerPixel: 32, bytesPerRow: width * 4, space: CGColorSpaceCreateDeviceRGB(),
                    bitmapInfo: CGBitmapInfo(rawValue: CGImageAlphaInfo.premultipliedLast.rawValue),
                    provider: provider, decode: nil, shouldInterpolate: false, intent: .defaultIntent) {
            bitmap.image = UIImage(cgImage: image)
        }
    }
}
