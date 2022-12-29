#!/usr/bin/env /usr/bin/python3

import sys

def n(r, c):
    return (r - 1) * (c - 1) + (r - 1) * r // 2 + (c - 1) * c // 2 + c

steps = n(2978, 3083)

code = 20151125

for _ in range(steps - 1):
    code = (code * 252533) % 33554393

print(code)
