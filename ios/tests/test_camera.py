#!/usr/bin/env python3
"""Exercise the shared ROM patch switch without distributing game data."""
from pathlib import Path
import re
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
patch = (root / 'ios/scripts/core-ios.patch').read_text()
source = '\n'.join(line[1:] for line in patch.splitlines()
                   if line.startswith('+') and not line.startswith('+++'))
table = re.search(r'static const struct \{ UINT32 address; UINT16 normal, wide; \} hangtime_patches\[\] =\n\{.*?\n\};', source, re.S).group()
switch = re.search(r'static void hangtime_apply_widescreen\(void\)\n\{.*?\n\}', source, re.S).group()
test = r'''
#include <assert.h>
#include <stdint.h>
typedef uint32_t UINT32;
typedef uint16_t UINT16;
static UINT16 rom[0x80000], ram[0x40000];
#define HT_ROM(a) rom[((a)-0xff800000u)>>4]
#define HT_RAM(a) ram[((a)-0x01000000u)>>4]
#define HT_SCRNTL 0x01002140u
#define HT_SCRNLR 0x01002160u
static int hangtime_requested, hangtime_wide;
static struct { struct { int min_y, max_y; } visible_area; } machine;
#define Machine (&machine)
static void hangtime_move_plates(int wide) { (void)wide; }
static void set_visible_area(int x0,int x1,int y0,int y1) {
    assert(x0==0 && x1==(hangtime_requested ? 511 : 399));
    (void)y0; (void)y1;
}
'''
test += table + '\n' + switch + r'''
int main(void) {
    const UINT32 inbound[] = {0xff904f20u,0xff904fc0u,0xff908e30u,0xff908e70u};
    const UINT16 original[] = {0x1dd0,0x20a0,0x1dc1,0x20af};
    /* General tracking and dunk limits must remain the original arcade words. */
    const UINT32 tracking[] = {0xff909700u,0xff909730u,0xff909760u,0xff909790u,
        0xff9099e0u,0xff909ab0u,0xff9093a0u,0xff9093e0u};
    const UINT16 limits[] = {0xe137,0x1ec8,0xdec7,0x2138,0xe23e,0xdf50,0x1dd5,0x209b};
    unsigned i;
    for(i=0;i<sizeof(hangtime_patches)/sizeof(hangtime_patches[0]);i++)
        HT_ROM(hangtime_patches[i].address)=hangtime_patches[i].normal;
    for(i=0;i<8;i++) HT_ROM(tracking[i])=limits[i];
    for(i=0;i<4;i++) assert(HT_ROM(inbound[i])==original[i]);
    /* Switching live, repeatedly, must restore 4:3 and preserve both court ends. */
    for(unsigned cycle=0;cycle<10;cycle++) {
        hangtime_requested=1; hangtime_apply_widescreen(); assert(hangtime_wide==1);
        for(i=0;i<4;i++) {
            int wide=HT_ROM(inbound[i]);
            assert(wide-original[i]==((i%2) ? -56 : 56));
            /* A 56-pixel wider outer edge lands at the original scenery boundary. */
            assert(wide+((i%2) ? 56 : -56)==original[i]);
        }
        for(i=0;i<8;i++) assert(HT_ROM(tracking[i])==limits[i]);
        hangtime_requested=0; hangtime_apply_widescreen(); assert(hangtime_wide==0);
        for(i=0;i<4;i++) assert(HT_ROM(inbound[i])==original[i]);
        for(i=0;i<8;i++) assert(HT_ROM(tracking[i])==limits[i]);
    }
}
'''
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    (path / 'camera.c').write_text(test)
    subprocess.run(['clang', '-fsanitize=address,undefined', str(path / 'camera.c'),
                    '-o', str(path / 'camera')], check=True)
    subprocess.run([str(path / 'camera')], check=True)
print('Inbound scenery bounds, corner tracking and live widescreen switching passed.')
