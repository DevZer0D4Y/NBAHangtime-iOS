#!/usr/bin/env python3
"""Exercise the privacy gate with release payloads and injected metadata."""
from pathlib import Path
import io
import sys
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from release_hygiene import check_archive, check_payload


class ReleaseHygieneTests(unittest.TestCase):
    def test_release_content_allowed(self):
        check_payload('Payload/Hangtime.app/Hangtime', b'\xcf\xfa\xed\xfe\x00Game code')
        check_payload('README.md', b'https://github.com/example/project\nCopyright Project Authors')

    def test_home_paths_rejected_inside_binary(self):
        for path in [b'/Users/example/build/main.o', b'/home/example/build/main.o',
                     b'C:\\Users\\example\\build\\main.obj', b'C:/Users/example/build/main.obj',
                     b'/private/var/folders/example/build/main.o']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                check_payload('Hangtime', b'\x00\x01' + path + b'\x00')

    def test_private_key_rejected(self):
        with self.assertRaises(ValueError):
            check_payload('settings.txt', b'-----BEGIN OPENSSH PRIVATE KEY-----')

    def test_unintended_files_rejected(self):
        for name in ['Payload/Hangtime.app/embedded.mobileprovision', 'certificate.p12',
                     'nbahangt.zip', 'htime54.bin', 'build.log', 'Hangtime.pdb',
                     '.git/config', 'xcuserdata/state', 'Hangtime.dSYM/Contents/Info.plist']:
            with self.subTest(name=name), self.assertRaises(ValueError):
                check_payload(name, b'contents')

    def test_every_archive_entry_is_checked(self):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            archive.writestr('NBA Hangtime.exe', b'clean binary')
            archive.writestr('SDL2.dll', b'\x00/home/example/toolchain\x00')
        with zipfile.ZipFile(stream) as archive, self.assertRaises(ValueError):
            check_archive(archive)


if __name__ == '__main__':
    unittest.main(verbosity=2)
