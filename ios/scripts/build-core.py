#!/usr/bin/env python3
"""Pinned, isolated static builds; one object tree per Apple SDK/architecture."""
import os
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PIN = 'e05caba0aa33cae580d104c45c6caa6406617e3b'
VENDOR = ROOT / 'vendor/mame2003-plus'
sdk = os.environ.get('PLATFORM_NAME', sys.argv[1] if len(sys.argv) > 1 else 'iphonesimulator')
if os.environ.get('CURRENT_ARCH', 'undefined_arch') == 'undefined_arch' and os.environ.get('ARCHS'):
    for build_arch in os.environ['ARCHS'].split():
        env = dict(os.environ, CURRENT_ARCH=build_arch)
        subprocess.run([sys.executable, str(Path(__file__).resolve()), sdk], env=env, check=True)
    sys.exit(0)
arch = os.environ.get('CURRENT_ARCH', 'arm64')
if arch == 'undefined_arch': arch = 'arm64'
if sdk not in ('iphoneos', 'iphonesimulator') or arch not in ('arm64', 'x86_64'):
    raise SystemExit('Unsupported SDK/architecture: ' + sdk + '/' + arch)
if not (VENDOR / 'Makefile').exists():
    subprocess.run(['git', 'clone', 'https://github.com/libretro/mame2003-plus-libretro.git', str(VENDOR)], check=True)
    subprocess.run(['git', '-C', str(VENDOR), 'checkout', PIN], check=True)
actual = subprocess.check_output(['git', '-C', str(VENDOR), 'rev-parse', 'HEAD'], text=True).strip()
if actual != PIN: raise SystemExit('Core checkout differs from pinned revision: ' + actual)
# Apply the tracked patch once; reject unexpected modifications instead of silently changing source.
patch = ROOT / 'ios/scripts/core-ios.patch'
check = subprocess.run(['git', '-C', str(VENDOR), 'apply', '--reverse', '--check', str(patch)], capture_output=True)
if check.returncode:
    if subprocess.run(['git', '-C', str(VENDOR), 'apply', str(patch)]).returncode:
        raise SystemExit('vendor/mame2003-plus has other changes, such as an older version of the patch. '
                         'Reset it with: git -C vendor/mame2003-plus checkout -- .')
output = ROOT / 'ios/Core' / ('libhangtime-' + sdk + '-' + arch + '.a')
build = ROOT / 'ios/.build' / (sdk + '-' + arch)
if output.exists() and output.stat().st_mtime > max(patch.stat().st_mtime, Path(__file__).stat().st_mtime):
    print('Core up to date:', output.name); sys.exit(0)
fingerprint = hashlib.sha256(patch.read_bytes() + Path(__file__).read_bytes()).hexdigest()
stamp = build / '.hangtime-build-fingerprint'
if not stamp.exists() or stamp.read_text() != fingerprint:
    if build.exists(): shutil.rmtree(build)
    shutil.copytree(VENDOR, build, ignore=shutil.ignore_patterns('.git', '*.o', '*.a', '*.dylib'))
    stamp.write_text(fingerprint)
sdkpath = subprocess.check_output(['xcrun', '--sdk', sdk, '--show-sdk-path'], text=True).strip()
cc = subprocess.check_output(['xcrun', '--sdk', sdk, '--find', 'clang'], text=True).strip()
triple = arch + '-apple-ios16.0' + ('-simulator' if sdk == 'iphonesimulator' else '')
output.parent.mkdir(parents=True, exist_ok=True)
# Two low-priority jobs by default keeps the machine usable; HANGTIME_BUILD_JOBS overrides it.
args = ['nice', '-n', '19', 'make', '-j' + os.environ.get('HANGTIME_BUILD_JOBS', '2'), 'platform=osx', 'INCLUDE_DRV=drv_hangtime',
        'STATIC_LINKING=1', 'TARGET=' + str(output), 'CC=' + cc + ' -target ' + triple + ' -isysroot ' + sdkpath,
        'PLATCFLAGS=-Ddrv_hangtime -DSPLIT_CORE -Wno-error=implicit-function-declaration -Wno-error=int-conversion -Wno-error=incompatible-pointer-types']
log = ROOT / 'ios' / ('core-' + sdk + '-' + arch + '.log')
with log.open('w') as stream:
    result = subprocess.run(args, cwd=build, stdout=stream, stderr=subprocess.STDOUT)
if result.returncode:
    print(log.read_text()[-12000:]); raise SystemExit(result.returncode)
print('Built', output)
