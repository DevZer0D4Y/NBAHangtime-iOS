"""Reject private build metadata and unintended files in release payloads."""
from pathlib import PurePosixPath
import re

_HOME_PATH = re.compile(rb'(?:/Users/|/home/|/private/var/folders/|[A-Za-z]:[\\/]Users[\\/])', re.I)
_PRIVATE_KEY = re.compile(rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----')
_FORBIDDEN_SUFFIXES = {
    '.zip', '.bin', '.rom', '.u54', '.u63', '.nv',
    '.o', '.a', '.pdb', '.log', '.swiftmodule', '.swiftdoc',
    '.c', '.h', '.swift', '.py', '.metal', '.glsl',
    '.mobileprovision', '.p12', '.pfx', '.pem', '.key', '.cer', '.crt',
}
_FORBIDDEN_PARTS = {'.git', '.env', '.DS_Store', '__pycache__', 'xcuserdata', '_CodeSignature'}


def check_payload(name, data):
    path = PurePosixPath(name)
    if path.suffix.lower() in _FORBIDDEN_SUFFIXES or any(
        part in _FORBIDDEN_PARTS or part.endswith(('.dSYM', '.xcodeproj')) for part in path.parts
    ):
        raise ValueError(f'Unintended release file: {name}')
    if _HOME_PATH.search(data):
        raise ValueError(f'Home-directory build path in release file: {name}')
    if _PRIVATE_KEY.search(data):
        raise ValueError(f'Private key in release file: {name}')


def check_archive(archive):
    for entry in archive.infolist():
        if not entry.is_dir():
            check_payload(entry.filename, archive.read(entry))
