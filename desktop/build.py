#!/usr/bin/env python3
"""Build the shared Hangtime SDL frontend for Windows x64 or the local host."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
parser=argparse.ArgumentParser()
parser.add_argument('--windows',action='store_true')
parser.add_argument('--cc')
parser.add_argument('--ar')
parser.add_argument('--windres')
parser.add_argument('--sdl-prefix',type=Path)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
vendor=root/'vendor/mame2003-plus'
pin='e05caba0aa33cae580d104c45c6caa6406617e3b'
if not (vendor/'Makefile').exists():
    subprocess.run(['git','clone','https://github.com/libretro/mame2003-plus-libretro.git',str(vendor)],check=True)
    subprocess.run(['git','-C',str(vendor),'checkout',pin],check=True)
actual=subprocess.check_output(['git','-C',str(vendor),'rev-parse','HEAD'],text=True).strip()
if actual!=pin: raise SystemExit('Unexpected core revision '+actual)
patch=root/'ios/scripts/core-ios.patch'
if subprocess.run(['git','-C',str(vendor),'apply','--reverse','--check',str(patch)],capture_output=True).returncode:
    if subprocess.run(['git','-C',str(vendor),'apply',str(patch)]).returncode:
        raise SystemExit('vendor/mame2003-plus has other changes, such as an older version of the patch. '
                         'Reset it with: git -C vendor/mame2003-plus checkout -- .')
windows=args.windows or sys.platform=='win32'
name='windows-x64' if windows else 'native'
toolchain=root/'vendor/llvm-mingw-20260616-ucrt-macos-universal/bin'
cc=args.cc or (str(toolchain/'x86_64-w64-mingw32-clang') if windows and toolchain.exists() else 'gcc' if windows else 'clang')
ar=args.ar or (str(toolchain/'llvm-ar') if windows and toolchain.exists() else 'ar')
build=root/'desktop/.build'/name
fingerprint=hashlib.sha256(patch.read_bytes()+Path(__file__).read_bytes()+cc.encode()).hexdigest()
stamp=build/'.build-fingerprint'
if not stamp.exists() or stamp.read_text()!=fingerprint:
    if build.exists(): shutil.rmtree(build)
    shutil.copytree(vendor,build,ignore=shutil.ignore_patterns('.git','metadata','*.o','*.a','*.dll','*.dylib'))
    stamp.write_text(fingerprint)
output=root/'dist'/name
output.mkdir(parents=True,exist_ok=True)
library=build/'libhangtime.a'
# Two jobs by default keeps the machine usable; HANGTIME_BUILD_JOBS overrides it.
make=['make','-j'+os.environ.get('HANGTIME_BUILD_JOBS','2'),'platform=win' if windows else 'platform=osx',
      'INCLUDE_DRV=drv_hangtime','STATIC_LINKING=1','TARGET='+str(library),'CC='+cc,'AR='+ar,
      'PLATCFLAGS=-Ddrv_hangtime -DSPLIT_CORE -Wno-error=implicit-function-declaration -Wno-error=int-conversion -Wno-error=incompatible-pointer-types']
if windows: make+=['system_platform=win','SPLIT_UP_LINK=0']
log=root/'desktop'/('build-'+name+'.log')
with log.open('w') as stream:
    result=subprocess.run(make,cwd=build,stdout=stream,stderr=subprocess.STDOUT)
if result.returncode: print(log.read_text()[-16000:]); raise SystemExit(result.returncode)
common=root/'ios/Hangtime'
command=[cc,'-O2','-I'+str(common),'-I'+str(vendor/'src/libretro-common/include'),'-I'+str(vendor/'src/lib/zlib')]
if windows:
    sdl=(args.sdl_prefix or root/'vendor/SDL2-2.32.10/x86_64-w64-mingw32').resolve()
    command+=['-I'+str(sdl/'include/SDL2'),'-L'+str(sdl/'lib')]
else:
    command+=subprocess.check_output(['sdl2-config','--cflags'],text=True).split()
command+=[str(root/'desktop/main.c'),str(common/'HangtimeCore.c'),str(common/'ROMAudit.c'),str(library)]
if windows:
    # Icon and version details, so Explorer and Task Manager show "NBA Hangtime".
    windres=args.windres or (str(toolchain/'x86_64-w64-mingw32-windres') if toolchain.exists() else cc.replace('clang','windres').replace('gcc','windres'))
    resource=build/'hangtime-resource.o'
    subprocess.run([windres,'-I',str(root/'desktop'),str(root/'desktop/hangtime.rc'),'-O','coff','-o',str(resource)],check=True)
    command.append(str(resource))
if windows: command+=['-mwindows','-lSDL2','-lcomdlg32','-lws2_32','-lole32','-lshell32','-luuid','-lm','-o',str(output/'NBA Hangtime.exe')]
else: command+=subprocess.check_output(['sdl2-config','--libs'],text=True).split()+['-lz','-o',str(output/'Hangtime')]
subprocess.run(command,check=True)
if windows:
    shutil.copy2(sdl/'bin/SDL2.dll',output/'SDL2.dll')
    for license_path in (sdl.parent/'LICENSE.txt', sdl/'share/licenses/SDL2/LICENSE'):
        if license_path.exists():
            shutil.copy2(license_path,output/'SDL-LICENSE.txt')
            break
shutil.copy2(vendor/'LICENSE.md',output/'MAME-LICENSE.md')
shutil.copy2(root/'desktop/README.md',output/'README.md')
print('Built',output)
