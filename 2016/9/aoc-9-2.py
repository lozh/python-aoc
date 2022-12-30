#!/usr/bin/env /usr/bin/python3

import sys
import re

marker_re = re.compile("\((\d+)x(\d+)\)")
def decomp_len(s):
    length = 0
    while m := marker_re.search(s):
        b, e = m.span(0)
        length += b
        l = int(m.group(1))
        r = int(m.group(2))
        length += r * decomp_len(s[e:e + l])
        s = s[e + l:]
    length += len(s)
    return length

i = sys.stdin.readline().strip()

print(decomp_len(i))
