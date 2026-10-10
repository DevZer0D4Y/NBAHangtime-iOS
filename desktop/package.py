#!/usr/bin/env python3
"""Package the Windows build into a release ZIP. Only the listed files are included: never game ROMs."""
from pathlib import Path
import hashlib
import shutil
import zipfile

root=Path(__file__).resolve().parents[1]
folder=root/'dist/windows-x64'
required=['NBA Hangtime.exe','SDL2.dll','README.md','MAME-LICENSE.md','SDL-LICENSE.txt']
shutil.copy2(root/'desktop/README.md',folder/'README.md')
sdl_license=root/'vendor/SDL2-2.32.10/LICENSE.txt'
if sdl_license.exists(): shutil.copy2(sdl_license,folder/'SDL-LICENSE.txt')
for name in required:
    if not (folder/name).is_file(): raise SystemExit('Missing Windows release file: '+name)
archive=root/'dist/NBA-Hangtime-Windows-x64.zip'
top='NBA-Hangtime-Windows-x64'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as package:
    for name in required: package.write(folder/name,top+'/'+name)
with zipfile.ZipFile(archive) as package:
    failure=package.testzip()
    if failure: raise SystemExit('Corrupt package entry: '+failure)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.sha256').write_text(digest+'  '+archive.name+'\n')
print(archive)
print('ZIP integrity passed; SHA256:',digest)
