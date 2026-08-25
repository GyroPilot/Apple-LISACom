#!/usr/bin/env python3
import sys
src, dst = sys.argv[1], sys.argv[2]
data = open(src, 'rb').read()
data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
lines = data.split(b'\n')
if lines and lines[-1] == b'':
    lines.pop()
pages = []
cur = b''
for ln in lines:
    rec = ln + b'\r'
    if len(rec) > 1024:
        sys.exit(f'line longer than a page: {len(rec)} bytes')
    if len(cur) + len(rec) > 1024:
        pages.append(cur + b'\x00' * (1024 - len(cur)))
        cur = b''
    cur += rec
if cur:
    pages.append(cur + b'\x00' * (1024 - len(cur)))
out = b'\x00' * 1024 + b''.join(pages)
open(dst, 'wb').write(out)
print(f'{src}: {len(lines)} lines -> {len(pages)} text pages')
