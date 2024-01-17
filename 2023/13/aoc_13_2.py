#!/usr/bin/env python3
import sys
from itertools import product

def find_vertical_mirror(layout):
    l = len(layout[0])
    for i in range(l - 1):
        ml = min(i + 1, l - i - 1)
        match = True
        for j in range(ml):
            c1 = [x[i - j] for x in layout]
            c2 = [x[i + j + 1] for x in layout]
            if c1 != c2:
                match = False
                break
        if match:
            yield i

def find_horizontal_mirror(layout):
    l = len(layout)
    for i in range(l - 1):
        # how many lines do we need to check for a perfect mirror
        ml = min(i + 1, l - i - 1)
        match = True
        for j in range(ml):
            if layout[i - j] != layout [i + j + 1]:
                match = False
                break
        if match:
            yield i

def score(layout):
    for s in find_horizontal_mirror(layout):
        os = s
        is_h = True
    for s in find_vertical_mirror(layout):
        os = s
        is_h = False
        
    for l in permute(layout):
        for s in find_horizontal_mirror(l):
            if not (is_h and s == os):
                return 100 * (s + 1)
        for s in find_vertical_mirror(l):
            if not (not is_h and s == os):
                return s + 1
    raise ValueError("No Answer")

def permute(layout):
    height = len(layout)
    width = len(layout[0])
    for i, j in product(range(width), range(height)):
        layout[j][i] = not layout[j][i]
        yield layout
        layout[j][i] = not layout[j][i]

def lines_to_maps(lines):
    m = []
    for line in lines:
        if line:
            m.append(list(map(lambda c: c == '#', line)))
        else:
            yield m
            m = []
    yield m

lines = map(str.rstrip, sys.stdin)
maps = lines_to_maps(lines)
print(sum(map(score, maps)))
