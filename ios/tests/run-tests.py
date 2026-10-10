#!/usr/bin/env python3
"""Run importer tests and the isolated native bridge with ASan and UBSan."""
from pathlib import Path
import subprocess
import sys
import tempfile
root = Path(__file__).resolve().parents[2]
subprocess.run([sys.executable, str(root / 'ios/tests/test_rom_audit.py')], check=True)
with tempfile.TemporaryDirectory(dir=root / 'ios') as temp:
    executable = Path(temp) / 'core-tests'
    subprocess.run(['clang', '-fsanitize=address,undefined',
                    '-I' + str(root / 'ios/Hangtime'),
                    '-I' + str(root / 'vendor/mame2003-plus/src/libretro-common/include'),
                    str(root / 'ios/Hangtime/HangtimeCore.c'),
                    str(root / 'ios/tests/test_core_bridge.c'), '-o', str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
