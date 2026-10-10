#!/usr/bin/env python3
"""Package the Windows build into a release ZIP. Only the listed files are included: never game ROMs."""
from pathlib import Path
import argparse
import hashlib
import shutil
import subprocess
import sys
import zipfile

root=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'scripts'))
from release_hygiene import check_archive, check_payload
parser=argparse.ArgumentParser()
parser.add_argument('--strip', help='Path to a COFF-capable llvm-strip or MinGW strip')
args=parser.parse_args()
folder=root/'dist/windows-x64'
required=['NBA Hangtime.exe','SDL2.dll','README.md','MAME-LICENSE.md','SDL-LICENSE.txt',
          'LICENSE-MIT.txt','SOURCE.md','RELEASE-NOTES.md']
shutil.copy2(root/'desktop/README.md',folder/'README.md')
shutil.copy2(root/'LICENSE',folder/'LICENSE-MIT.txt')
for name in ('SOURCE.md', 'RELEASE-NOTES.md'):
    shutil.copy2(root/name,folder/name)
sdl_license=root/'vendor/SDL2-2.32.10/LICENSE.txt'
if sdl_license.exists(): shutil.copy2(sdl_license,folder/'SDL-LICENSE.txt')
for name in required:
    if not (folder/name).is_file(): raise SystemExit('Missing Windows release file: '+name)
bundled=root/'vendor/llvm-mingw-20260616-ucrt-macos-universal/bin/llvm-strip'
strip_tool=args.strip or (str(bundled) if bundled.is_file() else
                         shutil.which('x86_64-w64-mingw32-strip') or shutil.which('llvm-strip') or
                         (shutil.which('strip') if sys.platform=='win32' else None))
if not strip_tool: raise SystemExit('A COFF-capable strip tool is required; pass --strip /path/to/llvm-strip.')
subprocess.run([strip_tool, '--strip-debug', str(folder/'NBA Hangtime.exe'), str(folder/'SDL2.dll')], check=True)
for name in required: check_payload(name, (folder/name).read_bytes())
archive=root/'dist/NBA-Hangtime-Windows-x64.zip'
top='NBA-Hangtime-Windows-x64'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as package:
    for name in required: package.write(folder/name,top+'/'+name)
with zipfile.ZipFile(archive) as package:
    failure=package.testzip()
    if failure: raise SystemExit('Corrupt package entry: '+failure)
    check_archive(package)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.sha256').write_text(digest+'  '+archive.name+'\n')
print(archive)
print('ZIP integrity passed; SHA256:',digest)
