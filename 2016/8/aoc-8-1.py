#!/usr/bin/env /usr/bin/python3

import sys
import re
from itertools import repeat

def rect(screen, a, b):
    for x in range(a):
        for y in range(b):
            screen[y][x] = True
    return screen

def rotate_list(l, n):
    n = (-n) % len(l)
    return l[n:] + l[:n]

def rotate_row(screen, a, b):
    screen[a] = rotate_list(screen[a], b)
    return screen

def rotate_col(screen, a, b):
    col = [row[a] for row in screen]
    new_col = rotate_list(col, b)
    for row, c  in zip(screen, new_col):
        row[a] = c
    return screen

def print_screen(screen):
    for l in screen:
        print("".join("#" if p else "." for p in l))
    print()

rect_re = re.compile("^rect (\d+)x(\d+)$")
ror_re = re.compile("^rotate row y=(\d+) by (\d+)$")
roc_re = re.compile("^rotate column x=(\d+) by (\d+)$")

def apply(screen, instruction):
    if m:= rect_re.match(instruction):
        return rect(screen, int(m.group(1)), int(m.group(2)))
    if m:= ror_re.match(instruction):
        return rotate_row(screen, int(m.group(1)), int(m.group(2)))
    if m:= roc_re.match(instruction):
        return rotate_col(screen, int(m.group(1)), int(m.group(2)))
    raise Exception(f"Did not recognise {instruction}")

rows = 6
cols = 50
screen = []
for _ in range(rows):
    screen.append(list(repeat(False, cols)))

for i in sys.stdin:
    screen = apply(screen, i)

print(sum(1 for l in screen for p in l if p))
