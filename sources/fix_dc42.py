#!/usr/bin/env python3
"""fix_dc42.py IN.dc42 OUT.dc42 -- recompute the DiskCopy 4.2 data and tag checksums
(Apple convention: tag checksum skips the first 12 tag bytes).  Nothing else is touched."""
import sys, struct
def cs(b):
    c = 0
    for i in range(0, len(b) - 1, 2):
        c = (c + ((b[i] << 8) | b[i + 1])) & 0xffffffff
        c = ((c >> 1) | ((c & 1) << 31)) & 0xffffffff
    return c
d = bytearray(open(sys.argv[1], 'rb').read())
dsize, tsize = struct.unpack(">II", d[0x40:0x48])
data = d[0x54:0x54 + dsize]; tags = d[0x54 + dsize:0x54 + dsize + tsize]
old = struct.unpack(">II", d[0x48:0x50])
new = (cs(data), cs(tags[12:]) if tsize else 0)
d[0x48:0x50] = struct.pack(">II", *new)
open(sys.argv[2], 'wb').write(d)
print(f"data {old[0]:08x} -> {new[0]:08x}, tags {old[1]:08x} -> {new[1]:08x}, {len(d)} bytes")
