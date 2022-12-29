#!/usr/bin/env /usr/bin/python3

import sys

buttons = [
    [' ', ' ', '1', ' ', ' '],
    [' ', '2', '3', '4', ' '],
    ['5', '6', '7', '8', '9'],
    [' ', 'A', 'B', 'C', ' '],
    [' ', ' ', 'D', ' ', ' '],
]

offsets = {
    'U': (0, -1),
    'D': (0, 1),
    'R': (1, 0),
    'L': (-1, 0)
}

pos = (0, 2)

def bound(x):
    if x < 0:
        return 0
    if x > 4:
        return 4
    return x

ans = ""

for instructions in map(str.rstrip, sys.stdin):
    while instructions:
        i, *instructions = instructions
        o = offsets[i]
        new_pos = bound(pos[0] + o[0]), bound(pos[1] + o[1])
        if buttons[new_pos[1]][new_pos[0]] != ' ':
            pos = new_pos
    ans += f"{buttons[pos[1]][pos[0]]}"

print(ans)
