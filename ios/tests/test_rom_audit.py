#!/usr/bin/env python3
"""Host-side tests of the same C ROM importer used by the iOS app.

No game data is needed: each stand-in ROM is zeros plus four bytes chosen so the file has the
size and CRC32 of the real one, which is all the importer can check."""
import ctypes
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = json.loads((ROOT / 'ios/rom-manifest.json').read_text())

TABLE = []
for index in range(256):
    value = index
    for _ in range(8):
        value = (value >> 1) ^ (0xEDB88320 if value & 1 else 0)
    TABLE.append(value)
INVERSE = {entry >> 24: index for index, entry in enumerate(TABLE)}

def stand_in(size, crc):
    """Zeros whose last four bytes make the CRC32 equal crc (run the CRC backwards from the target)."""
    prefix = bytes(size - 4)
    register = crc ^ 0xFFFFFFFF
    for _ in range(4):
        index = INVERSE[register >> 24]
        register = ((register ^ TABLE[index]) << 8 & 0xFFFFFFFF) | index
    return prefix + (register ^ zlib.crc32(prefix) ^ 0xFFFFFFFF).to_bytes(4, 'little')

def rom(name):
    entry = next(item for item in MANIFEST if item['name'] == name)
    data = stand_in(entry['size'], int(entry['crc'], 16))
    assert zlib.crc32(data) == int(entry['crc'], 16)
    return data

class ROMAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        zlib_sources = ROOT / 'vendor/mame2003-plus/src/lib/zlib'
        if not zlib_sources.is_dir():
            raise SystemExit('Fetch the pinned core first (see README.md, "Building").')
        cls.temp = tempfile.TemporaryDirectory()
        cls.work = Path(cls.temp.name)
        lib = cls.work / 'audit.dylib'
        subprocess.run(['clang', '-dynamiclib', '-I' + str(ROOT / 'ios/Hangtime'), '-I' + str(zlib_sources),
                        str(ROOT / 'ios/Hangtime/ROMAudit.c'), str(zlib_sources / 'unzip.c'), str(zlib_sources / 'ioapi.c'),
                        '-lz', '-o', str(lib)], check=True)
        cls.lib = ctypes.CDLL(str(lib))
        cls.lib.ht_validate_rom.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
        cls.lib.ht_validate_rom.restype = ctypes.c_bool
    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()
    def validate(self, path, capacity=8192):
        report = ctypes.create_string_buffer(capacity)
        valid = self.lib.ht_validate_rom(str(path).encode(), report, capacity)
        return valid, report.value.decode()
    def program_zip(self, filename='program.zip', compression=zipfile.ZIP_DEFLATED):
        path = self.work / filename
        with zipfile.ZipFile(path, 'w', compression) as z:
            # CRC lookup accepts any file names, including folders inside the archive.
            z.writestr('nested/historical.u54', rom('htime54.bin'))
            z.writestr('nested/historical.u63', rom('htime63.bin'))
        return path
    def test_missing_file(self):
        ok, report = self.validate(self.work / 'absent.zip')
        self.assertFalse(ok); self.assertIn('ZIP', report)
    def test_invalid_zip(self):
        path = self.work / 'invalid.zip'; path.write_bytes(b'not a zip')
        self.assertFalse(self.validate(path)[0])
    def test_complete_set_accepted(self):
        path = self.work / 'complete.zip'
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
            for entry in MANIFEST: z.writestr(entry['name'], rom(entry['name']))
        self.assertEqual((True, ''), self.validate(path))
    def test_program_found_by_crc_but_graphics_and_audio_missing(self):
        ok, report = self.validate(self.program_zip())
        self.assertFalse(ok)
        self.assertNotIn('htime54.bin', report); self.assertNotIn('htime63.bin', report)
        self.assertIn('mhtu2.bin', report); self.assertIn('mhtu133.bin', report)
        self.assertEqual(24, len(report.splitlines()) - 1)
    def test_wrong_revision_rejected(self):
        path = self.work / 'wrong.zip'
        with zipfile.ZipFile(path, 'w') as z: z.writestr('htime54.bin', stand_in(524288, 0x12345678))
        self.assertIn('htime54.bin', self.validate(path)[1])
    def test_payload_corruption_detected_even_with_valid_directory_crc(self):
        path = self.program_zip('corrupt.zip', zipfile.ZIP_STORED)
        data = bytearray(path.read_bytes())
        name_size, extra_size = struct.unpack_from('<HH', data, 26)
        data[30 + name_size + extra_size + 100] ^= 0xff
        path.write_bytes(data)
        ok, report = self.validate(path)
        self.assertFalse(ok); self.assertIn('htime54.bin', report); self.assertNotIn('htime63.bin', report)
    def test_small_report_buffer_terminated(self):
        ok, report = self.validate(self.program_zip('small.zip'), capacity=8)
        self.assertFalse(ok); self.assertLessEqual(len(report), 7)

if __name__ == '__main__': unittest.main(verbosity=2)
