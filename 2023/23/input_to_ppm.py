#!/usr/bin/env python3

import sys

lines = list(map(str.rstrip, sys.stdin))

print("P3")
print(len(lines[0]), len(lines))
print(255)

char_map = {
    '#': (0, 0, 0),
    '.': (255, 255, 255),
    '>': (255, 0, 0),
    '<': (0, 255, 0),
    'v': (0, 0, 255),
    '^': (255, 255, 0)
}

for line in lines:
    for c in line:
        x, y, z = char_map[c]
        print(x, y, z)
