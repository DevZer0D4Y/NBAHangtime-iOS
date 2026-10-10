/* Integration test of the real arcade core with a user-provided ROM set.
   No game data is embedded; captures and NVRAM stay in the supplied directory. */
#include "HangtimeCore.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

extern unsigned char *generic_nvram;
extern size_t generic_nvram_size;
static bool nvram_matches_file(const char *directory) {
    char path[4096];
    snprintf(path,sizeof path,"%s/mame2003-plus/nvram/nbahangt.nv",directory);
    FILE *file=fopen(path,"rb");
    if (!file || !generic_nvram || !generic_nvram_size) { if (file) fclose(file); return false; }
    unsigned char *data=malloc(generic_nvram_size);
    if (!data) { fclose(file); return false; }
    size_t count=fread(data,1,generic_nvram_size,file);
    bool same=count==generic_nvram_size && !memcmp(data,generic_nvram,count);
    free(data); fclose(file); return same;
}
static int capture(const char *directory, unsigned frame) {
    char path[4096];
    snprintf(path,sizeof path,"%s/frame-%04u.ppm",directory,frame);
    FILE *file=fopen(path,"wb");
    if (!file) return 0;
    unsigned w=ht_width(), h=ht_height();
    fprintf(file,"P6\n%u %u\n255\n",w,h);
    const uint8_t *pixels=ht_pixels();
    for (unsigned i=0;i<w*h;i++) fwrite(pixels+i*4,1,3,file);
    return fclose(file)==0;
}
int main(int argc,char **argv) {
    if (argc!=4 && argc!=5) { fprintf(stderr,"Usage: test-game nbahangt.zip save-directory capture-directory\n"); return 1; }
    if (!ht_start(argv[1],argv[2])) { fprintf(stderr,"Core load failed: %s\n",ht_error()); return 2; }
    if (argc==5 && !strcmp(argv[4],"--reload-check")) {
        if (!nvram_matches_file(argv[2])) { fprintf(stderr,"Persisted NVRAM was not reloaded byte-for-byte.\n"); ht_stop(); return 6; }
        puts("Persisted NVRAM reloaded byte-for-byte in a fresh process.");
    }
    printf("Core loaded. FPS %.6f, audio %.0f Hz\n",ht_fps(),ht_sample_rate()); fflush(stdout);
    unsigned nonblack_frames=0, changes=0, nonzero_audio=0;
    uint32_t last_hash=0;
    double peak=0;
    clock_t began=clock();
    for (unsigned frame=0;frame<3000;frame++) {
        uint16_t buttons=0;
        if (frame>=350 && frame<355) buttons|=1u<<2; /* Coin */
        if (frame>=400 && frame<405) buttons|=1u<<3; /* Start */
        if (frame>=500 && frame<1400 && frame%90<5) buttons|=1u<<8; /* Confirm / shoot */
        if (frame>=1400) {
            if ((frame/120)%2) buttons|=1u<<6; else buttons|=1u<<7;
            buttons|=1u<<0; /* Turbo */
            if (frame%70<5) buttons|=1u<<8;
            if (frame%110<5) buttons|=1u<<1;
        }
        ht_set_buttons(0,buttons); ht_run();
        unsigned count=ht_width()*ht_height();
        const uint8_t *pixels=ht_pixels();
        uint32_t hash=2166136261u; bool nonblack=false;
        for (unsigned i=0;i<count;i++) {
            hash=(hash^pixels[i*4])*16777619u;
            hash=(hash^pixels[i*4+1])*16777619u;
            hash=(hash^pixels[i*4+2])*16777619u;
            if (pixels[i*4] || pixels[i*4+1] || pixels[i*4+2]) nonblack=true;
        }
        if (nonblack) nonblack_frames++;
        if (frame && hash!=last_hash) changes++;
        last_hash=hash;
        float left[2048],right[2048];
        ht_audio_read(left,right,2048);
        for (unsigned i=0;i<2048;i++) {
            double l=fabs(left[i]),r=fabs(right[i]);
            if (l>0.00001 || r>0.00001) nonzero_audio++;
            if (l>peak) peak=l; if (r>peak) peak=r;
        }
        if (frame==180 || frame==600 || frame==1200 || frame==2000 || frame==2999) {
            if (!capture(argv[3],frame)) { fprintf(stderr,"Capture failed\n"); ht_stop(); return 3; }
            printf("Frame %u: %ux%u, hash %08x, audio peak %.4f\n",frame,ht_width(),ht_height(),hash,peak); fflush(stdout);
        }
        if (frame && frame%300==0 && !ht_save_data()) { fprintf(stderr,"NVRAM save failed: %s\n",ht_error()); ht_stop(); return 4; }
    }
    bool saved=ht_save_data();
    if (saved && !nvram_matches_file(argv[2])) { fprintf(stderr,"NVRAM disk content differs from live data.\n"); ht_stop(); return 7; }
    printf("Result: %u nonblack frames, %u changing frames, %u audible sample pairs, peak %.4f, saved %d, CPU %.2fs\n",nonblack_frames,changes,nonzero_audio,peak,saved,(double)(clock()-began)/CLOCKS_PER_SEC);
    ht_stop();
    if (!saved || changes<100 || nonblack_frames<100 || !nonzero_audio) { fprintf(stderr,"Integration expectations failed: %s\n",ht_error()); return 5; }
    puts("Real ROM/core integration passed."); return 0;
}
