#!/usr/bin/env python3
import sys

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
            return (match, i)
    return (False, None)

# returns (bool, int)
# bool is True if found
# int is the row
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
            return (match, i)
    return (False, None)

def score(layout):
    m, s = find_horizontal_mirror(layout)
    if m:
        return 100 * (s + 1)
    m, s = find_vertical_mirror(layout)
    if m:
        return s + 1
    print("No Score for layout")
    return None

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
