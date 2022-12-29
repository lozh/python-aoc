#!/usr/bin/env /usr/bin/python3

import sys

buttons = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

offsets = {
    'U': (0, -1),
    'D': (0, 1),
    'R': (1, 0),
    'L': (-1, 0)
}

pos = (1, 1)

def bound(x):
    if x < 0:
        return 0
    if x > 2:
        return 2
    return x
        
ans = ""

for instructions in map(str.rstrip, sys.stdin):
    while instructions:
        i, *instructions = instructions
        o = offsets[i]
        pos = bound(pos[0] + o[0]), bound(pos[1] + o[1])
    ans += f"{buttons[pos[1]][pos[0]]}"

print(ans)
