#!/usr/bin/env python3
"""Package an unsigned device build for local signing, without game ROMs."""
import hashlib
import json
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import zipfile

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / 'scripts'))
from release_hygiene import check_archive, check_payload
source = root / 'ios/DerivedDataDevice/Build/Products/Release-iphoneos/Hangtime.app'
info = plistlib.loads((source / 'Info.plist').read_bytes())
assert info['CFBundleIdentifier'] == 'com.devz.nbahangtime'
assert info['CFBundleDisplayName'] == 'NBA Hangtime'
assert info.get('CFBundleIcons'), 'App icon missing'
assert (source / 'Assets.car').is_file(), 'Compiled app icon missing'
assert (source / info['CFBundleExecutable']).read_bytes()[:4] == b'\xcf\xfa\xed\xfe', 'Device Mach-O missing'
for path in source.rglob('*'):
    assert not path.is_symlink(), f'Unexpected symlink: {path}'
    assert path.suffix.lower() not in {'.zip', '.bin', '.rom', '.u54', '.u63'}, f'Game file forbidden: {path}'
    assert 'nbahangt' not in path.name.lower(), f'Game file forbidden: {path}'
target = root / 'dist/iOS/Hangtime.app'
if target.exists():
    shutil.rmtree(target)
shutil.copytree(source, target)
shutil.copyfile(root / 'vendor/mame2003-plus/LICENSE.md', target / 'MAME-LICENSE.md')
shutil.copyfile(root / 'LICENSE', target / 'LICENSE-MIT.txt')
for name in ('SOURCE.md', 'RELEASE-NOTES.md'):
    shutil.copyfile(root / name, target / name)
# Unsigned payload only: discard debug records and local symbols containing build paths.
subprocess.run(['xcrun', 'strip', '-S', '-x', str(target / info['CFBundleExecutable'])], check=True)
for path in target.rglob('*'):
    if path.is_file():
        check_payload(path.relative_to(target).as_posix(), path.read_bytes())
output = root / 'dist/NBA-Hangtime-iOS.ipa'
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for path in sorted(target.rglob('*')):
        if path.is_file():
            archive.write(path, 'Payload/Hangtime.app/' + path.relative_to(target).as_posix())
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
    check_archive(archive)
    assert not any(name.lower().endswith(('.zip', '.bin', '.rom')) for name in archive.namelist())
checksum = hashlib.sha256(output.read_bytes()).hexdigest()
output.with_suffix('.sha256').write_text(checksum + '  ' + output.name + '\n')
print(json.dumps({'ipa': str(output), 'bytes': output.stat().st_size, 'sha256': checksum, 'roms_included': False, 'signed': False}, indent=2))
