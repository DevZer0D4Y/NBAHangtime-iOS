/* Test the actual OpenGL CRT passes, orientation, resizing and SDL overlays. */
#include "../CRTSDL.h"
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

int main(void) {
    assert(SDL_Init(SDL_INIT_VIDEO)==0);
    SDL_SetHint(SDL_HINT_RENDER_DRIVER,"opengl");
    SDL_Window *window=SDL_CreateWindow("CRT regression",0,0,640,480,SDL_WINDOW_HIDDEN);
    assert(window);
    SDL_Renderer *renderer=SDL_CreateRenderer(window,-1,SDL_RENDERER_ACCELERATED);
    assert(renderer);
    uint8_t *output=malloc(640*480*4); assert(output);
    for(unsigned cycle=0;cycle<6;cycle++) {
        unsigned w=cycle%2 ? 512 : 400,h=254;
        uint8_t *pixels=calloc(w*h,4); assert(pixels);
        for(unsigned y=0;y<h;y++) for(unsigned x=0;x<w;x++) {
            unsigned i=(y*w+x)*4;
            pixels[i]=y<h/2 ? 220 : 20;
            pixels[i+1]=((x/16)%2) ? 80 : 40;
            pixels[i+2]=y<h/2 ? 20 : 220;pixels[i+3]=255;
        }
        SDL_Texture *texture=SDL_CreateTexture(renderer,SDL_PIXELFORMAT_RGBA32,SDL_TEXTUREACCESS_STREAMING,w,h);
        assert(texture && SDL_UpdateTexture(texture,NULL,pixels,w*4)==0);
        SDL_Rect rect={0,0,640,480};
        crt_reset();
        SDL_SetRenderDrawColor(renderer,0,0,0,255);SDL_RenderClear(renderer);
        assert(crt_draw(renderer,texture,pixels,w,h,rect,true));
        assert(SDL_RenderReadPixels(renderer,NULL,SDL_PIXELFORMAT_RGBA32,output,640*4)==0);
        /* Strong color bands must retain their orientation through all four passes. */
        unsigned upper=(120*640+320)*4,lower=(360*640+320)*4;
        assert(output[upper]>output[upper+2] && output[lower+2]>output[lower]);
        /* Curved corners must be black even with bright source edge pixels. */
        unsigned corners[]={0,639*4,479*640*4,(480*640-1)*4};
        for(unsigned i=0;i<4;i++) {
            unsigned c=corners[i];
            assert(output[c]==0 && output[c+1]==0 && output[c+2]==0);
        }
        /* Turning CRT off restores exactly the original SDL picture. */
        SDL_RenderCopy(renderer,texture,NULL,&rect);
        assert(SDL_RenderReadPixels(renderer,NULL,SDL_PIXELFORMAT_RGBA32,output,640*4)==0);
        assert(output[upper]==220 && output[upper+2]==20);
        assert(output[lower]==20 && output[lower+2]==220);
        /* SDL menus must still draw over a CRT frame without a leaked shader. */
        assert(crt_draw(renderer,texture,pixels,w,h,rect,true));
        SDL_SetRenderDrawColor(renderer,12,200,35,255);
        SDL_Rect overlay={300,200,40,40};SDL_RenderFillRect(renderer,&overlay);
        assert(SDL_RenderReadPixels(renderer,NULL,SDL_PIXELFORMAT_RGBA32,output,640*4)==0);
        unsigned center=(220*640+320)*4;
        assert(output[center]==12 && output[center+1]==200 && output[center+2]==35);
        SDL_RenderPresent(renderer);SDL_DestroyTexture(texture);free(pixels);
    }
    crt_shutdown();free(output);SDL_DestroyRenderer(renderer);SDL_DestroyWindow(window);SDL_Quit();
    puts("OpenGL CRT: shader passes, image orientation, live toggles, 400/512 resizing and SDL overlays passed.");
}
