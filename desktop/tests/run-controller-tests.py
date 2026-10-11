#!/usr/bin/env python3
"""Test the SDL frontend's controller input with four virtual gamepads on the host."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
common = root / 'ios/Hangtime'
library = root / 'desktop/.build/native/libhangtime.a'
if not library.exists():
    raise SystemExit('Run python3 desktop/build.py first.')
with tempfile.TemporaryDirectory() as temp:
    executable = Path(temp) / 'controller-tests'
    command = ['clang', '-O2', '-I' + str(common),
               '-I' + str(root / 'vendor/mame2003-plus/src/libretro-common/include'),
               '-I' + str(root / 'vendor/mame2003-plus/src/lib/zlib')]
    command += subprocess.check_output(['sdl2-config', '--cflags'], text=True).split()
    command += [str(root / 'desktop/tests/test_controllers.c'), str(root / 'desktop/CRTSDL.c'),
                str(common / 'HangtimeCore.c'), str(common / 'ROMAudit.c'), str(library)]
    command += subprocess.check_output(['sdl2-config', '--libs'], text=True).split()
    import sys
    command += ['-framework', 'OpenGL'] if sys.platform == 'darwin' else ['-lGL']
    command += ['-lz', '-o', str(executable)]
    subprocess.run(command, check=True)
    subprocess.run([str(executable), str(Path(temp)) + "/"], check=True)
