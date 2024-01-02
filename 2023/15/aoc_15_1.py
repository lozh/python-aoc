#!/usr/bin/env python3

import sys

def hash(s):
    r = 0
    for c in s:
        r += ord(c)
        r *= 17
        r = r % 256
    return r

line = next(sys.stdin).rstrip()
print(sum(map(hash, line.split(","))))
