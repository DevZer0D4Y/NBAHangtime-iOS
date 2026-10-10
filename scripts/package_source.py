#!/usr/bin/env python3
"""Package tracked port files and the matching patched core, without local artifacts."""
import hashlib
from pathlib import Path
import plistlib
import subprocess
import zipfile

root = Path(__file__).resolve().parents[1]
core = root / 'vendor/mame2003-plus'
pin = 'e05caba0aa33cae580d104c45c6caa6406617e3b'
assert subprocess.check_output(['git', '-C', str(core), 'rev-parse', 'HEAD'], text=True).strip() == pin
subprocess.run(['git', '-C', str(core), 'apply', '--reverse', '--check',
                str(root / 'ios/scripts/core-ios.patch')], check=True)
version = plistlib.loads((root / 'ios/Hangtime/Info.plist').read_bytes())['CFBundleShortVersionString']
top = 'NBA-Hangtime-' + version + '-source'
output = root / 'dist' / (top + '.zip')
output.parent.mkdir(exist_ok=True)

def tracked(directory):
    return subprocess.check_output(['git', '-C', str(directory), 'ls-files', '-z']).decode().split('\0')[:-1]

forbidden = {'.zip', '.ipa', '.bin', '.rom', '.u54', '.u63', '.nv', '.o', '.a',
             '.dll', '.exe', '.log', '.p12', '.pfx', '.pem', '.key', '.mobileprovision'}
private_home = (str(Path.home()) + '/').encode()
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as package:
    for directory, prefix in ((root, ''), (core, 'vendor/mame2003-plus/')):
        for name in tracked(directory):
            # Upstream metadata artwork is unrelated to this driver's source build.
            if directory == core and name.startswith('metadata/'):
                continue
            path = directory / name
            assert path.is_file() and not path.is_symlink(), name
            assert path.suffix.lower() not in forbidden, name
            data = path.read_bytes()
            assert private_home not in data, name
            package.writestr(top + '/' + prefix + name, data)
    revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    package.writestr(top + '/SOURCE-REVISION.txt', 'Port: ' + revision + '\nCore: ' + pin + ' with core-ios.patch applied\n')
with zipfile.ZipFile(output) as package:
    assert package.testzip() is None
digest = hashlib.sha256(output.read_bytes()).hexdigest()
output.with_suffix('.sha256').write_text(digest + '  ' + output.name + '\n')
print(output)
print('Source archive integrity passed; SHA256:', digest)
