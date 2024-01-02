#!/usr/bin/env python3

import sys
from itertools import combinations

def get_galaxy_coordinates(lines):
    for (y, line) in enumerate(stdin):
        p = 0
        while p < len(line) and '#' in line[p:]:
            x = line.index('#', p)
            yield (x, y)
            p = x + 1

def find_empty_cols(coords, width):
    for i in range(width):
        if not any(True for (x, _) in coords if x == i):
            yield i

def find_empty_rows(coords, height):
    for j in range(height):
        if not any(True for (_, y) in coords if y == j):
            yield j

def explode_coord(x, y, empty_rows, empty_cols):
    nx = x + sum(1000000 - 1 for i in empty_cols if i < x)
    ny = y + sum(1000000 - 1 for j in empty_rows if j < y)
    # nx = x + sum(99 for i in empty_cols if i < x)
    # ny = y + sum(99 for j in empty_rows if j < y)
    return (nx, ny)

def explode(coords, empty_rows, empty_cols):
    yield from (explode_coord(x, y, empty_rows, empty_cols) for (x, y) in coords)

def distance(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    return abs(x2 - x1) + abs(y2 - y1)

stdin = map(str.rstrip, sys.stdin)

coords = list(get_galaxy_coordinates(stdin))
width = max(x for (x, _) in coords) + 1
height = max(y for (_, y) in coords) + 1

empty_cols = list(find_empty_cols(coords, width))
empty_rows = list(find_empty_rows(coords, height))

exploded = list(explode(coords, empty_rows, empty_cols))

print(sum(distance(x, y) for (x, y) in combinations(exploded, 2)))
