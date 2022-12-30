#!/usr/bin/env /usr/bin/python3

import sys
import re

# this is more than is strictly necessary
# we could just work out the length of the return
# instead of doing the decompression
marker_re = re.compile("\((\d+)x(\d+)\)")
def decomp(s):
    while m := marker_re.search(s):
        b, e = m.span(0)
        if b > 0:
            yield s[:b]
        l = int(m.group(1))
        r = int(m.group(2))
        for _ in range(r):
            yield s[e:e + l]
        s = s[e + l:]
    yield s

def decompress(s):
    return "".join(decomp(s))

i = sys.stdin.readline().strip()

print(len(decompress(i)))
