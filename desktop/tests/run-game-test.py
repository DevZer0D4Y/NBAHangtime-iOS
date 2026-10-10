#!/usr/bin/env python3
"""Exercise the real arcade core with supplied ROMs and verify NVRAM on restart."""
from pathlib import Path
import argparse
import subprocess
import sys
import struct
import zlib

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('rom',type=Path)
parser.add_argument('--work-dir',type=Path,default=root/'dist/validation')
parser.add_argument('--core-library',type=Path,default=root/'desktop/.build/native/libhangtime.a')
args=parser.parse_args()
rom=args.rom.resolve()
if not rom.is_file(): raise SystemExit('ROM ZIP not found: '+str(rom))
library=args.core_library.resolve()
if not library.is_file():
    subprocess.run([sys.executable,str(root/'desktop/build.py')],check=True)
    if not library.is_file(): raise SystemExit('Core library missing: '+str(library))
work=args.work_dir.resolve()
save=work/'save-data'
save.mkdir(parents=True,exist_ok=True)
executable=work/'test-game'
vendor=root/'vendor/mame2003-plus'
common=root/'ios/Hangtime'
subprocess.run(['clang','-O2','-I'+str(common),'-I'+str(vendor/'src/libretro-common/include'),
                '-I'+str(vendor/'src/lib/zlib'),str(common/'HangtimeCore.c'),str(common/'ROMAudit.c'),
                str(root/'desktop/tests/test_game.c'),str(library),'-lz','-o',str(executable)],check=True)
for name,extra in [('game-test.log',[]),('game-restart-test.log',['--reload-check'])]:
    with (work/name).open('w') as log:
        result=subprocess.run([str(executable),str(rom),str(save),str(work)]+extra,stdout=log,stderr=subprocess.STDOUT)
    print((work/name).read_text())
    if result.returncode: raise SystemExit(result.returncode)
for capture in work.glob('frame-*.ppm'):
    magic,dimension,maximum,pixels=capture.read_bytes().split(b'\n',3)
    width,height=map(int,dimension.split())
    if magic!=b'P6' or maximum!=b'255' or len(pixels)!=width*height*3: raise SystemExit('Bad capture: '+str(capture))
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    raw=b''.join(b'\0'+pixels[y*width*3:(y+1)*width*3] for y in range(height))
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')
    capture.with_suffix('.png').write_bytes(png)
print('ROM/core, audio, video and persisted NVRAM integration passed.')
