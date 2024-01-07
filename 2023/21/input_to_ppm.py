#!/usr/bin/env python3

import sys

print("P3")

lines = list(map(str.rstrip, sys.stdin))

print(len(lines[0]), len(lines))
print(255)

for line in lines:
    for c in line:
        match c:
            case '.':
                print(255, 255, 255)
            case '#':
                print(0, 0, 0)
            case 'S':
                print(255, 0, 0)
