#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as temp:
    executable = Path(temp) / 'crt-tests'
    command = ['clang', '-O2', str(root / 'desktop/tests/test_crt.c'), str(root / 'desktop/CRTSDL.c')]
    command += subprocess.check_output(['sdl2-config', '--cflags', '--libs'], text=True).split()
    command += ['-framework', 'OpenGL'] if sys.platform == 'darwin' else ['-lGL']
    subprocess.run(command + ['-o', str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
