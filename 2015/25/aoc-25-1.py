#!/usr/bin/env /usr/bin/python3

import sys

sys.setrecursionlimit(8000)

# There's probably a closed form for this, but it doesn't seem critical
def n(r, c):
    if r == 1 and c == 1:
        return 1
    if r == 1:
        return n(r, c - 1) + c
    if c == 1:
        return n(r - 1, c) + r - 1
    return n(r, c - 1) + r + c - 1


steps = n(2978, 3083)

code = 20151125

for _ in range(steps - 1):
    code = (code * 252533) % 33554393

print(code)
