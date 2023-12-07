"""
MIT License

Copyright (c) 2023 Eluli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
import hashlib
import shutil
import ctypes
import msvcrt

try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print("The tqdm module is not installed. You can install it by running 'pip install tqdm'.")
    exit(1)

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
FILE_FLAG_NO_BUFFERING = 0x20000000

def open_file_no_buffering(filename):
    CreateFile = ctypes.windll.kernel32.CreateFileW
    CreateFile.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p]
    CreateFile.restype = ctypes.c_void_p
    handle = CreateFile(filename, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, FILE_FLAG_NO_BUFFERING, None)
    if handle == -1:
        raise ctypes.WinError()
    fd = msvcrt.open_osfhandle(handle, 0)
    return open(fd, 'rb', buffering=0)

def write_random_file(folder, size, pbar):
    """Write a file with random content, return its name and md5 hash."""
    filename = os.path.join(folder, 'tempfile')
    hasher = hashlib.md5()
    with open(filename, 'wb') as f:
        for _ in range(size):
            buf = os.urandom(1048576)  # 1MB at a time
            f.write(buf)
            hasher.update(buf)
            pbar.update(1048576)
        f.flush()
        ctypes.windll.kernel32.FlushFileBuffers(f.fileno())
    md5_hash = hasher.hexdigest()
    new_filename = os.path.join(folder, md5_hash)
    os.rename(filename, new_filename)
    return new_filename, md5_hash

def verify_file(filename, md5_hash, pbar):
    """Verify a file against an md5 hash."""
    hasher = hashlib.md5()
    with open_file_no_buffering(filename) as f:
        while chunk := f.read(1048576):
            hasher.update(chunk)
            pbar.update(1048576)
    return hasher.hexdigest() == md5_hash

def test_sd_card_lifespan(folder):
    write_count = 0
    while True:
        try:
            file_hashes = []
            total_size = 1048576 * ((shutil.disk_usage(folder).free - 65536) // 1048576)
            if total_size < 1048576:
                print('Insufficient free space left on the device for further testing.')
                break
            n = total_size // (1024 * 1048576)  # Number of full 1024MB files
            remaining = (total_size % (1024 * 1048576)) // 1048576  # Size of the remaining file in MB
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="WRITE") as pbar:
                for _ in range(n):
                    filename, md5_hash = write_random_file(folder, 1024, pbar)
                    file_hashes.append((filename, md5_hash))
                if remaining > 0:
                    filename, md5_hash = write_random_file(folder, remaining, pbar)
                    file_hashes.append((filename, md5_hash))
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="READ ") as pbar:
                for filename, md5_hash in file_hashes:
                    assert verify_file(filename, md5_hash, pbar)
                    os.remove(filename)
            write_count += 1
            print(f'Successfully completed {write_count} write cycles.\n')
        except AssertionError:
            print(f'Encountered a validation error after completing {write_count} write cycles.')
            break
        except IOError:
            print(f'Encountered an I/O error after completing {write_count} write cycles.')
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lifespan.py <folder>")
        sys.exit(1)
    folder = sys.argv[1]
    test_sd_card_lifespan(folder)