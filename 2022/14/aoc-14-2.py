#!/usr/bin/env /usr/bin/python3

import sys
import re

def tuple_add(x, y):
    return tuple_map(sum, x, y)

# operate on tuples by element
def tuple_map(f, x, y):
    return tuple(map(f, zip(x, y)))

def cmp(x, y):
    return (x > y) - (x < y)

coord_re = re.compile("^(\d+),(\d+)$")
def parse_line(line):
    for coord in str.split(line, " -> "):
        m = coord_re.match(coord)
        yield int(m.group(1)), int(m.group(2))

def line_coords(start, end):
    x1, y1 = start
    x2, y2 = end

    offset = (cmp(x2, x1), cmp(y2, y1))
    yield start

    while True:
        start = tuple_add(start, offset) # add tuples elementwise
        yield start
        if start == end:
            break

# returns the next position for sand falling
# same as input if it doesn't move
def sand_next_pos(pos, grid):
    # possible routes down    
    offsets = [(0, 1), (-1, 1), (1, 1)]
    for offset in offsets:
        new_pos = tuple_add(pos, offset)
        if new_pos not in grid:
            return new_pos
    return pos

# Returns the position sand ends up in
def sand(start, grid, bottom):
    while True:
        pos = sand_next_pos(start, grid)
        if pos == start or pos[1] == bottom:
            return pos
        start = pos

# run the simulation
def simulate(entry, grid, bottom):
    i = 0
    while True:
        if entry in grid:
            # sand blocked
            return i
        s = sand(entry, grid, bottom)
        grid[s] = "."
        i += 1

grid = {}
entry = (500, 0)

# build grid. Just a map of (x, y) -> symbol
for line in map(str.rstrip, sys.stdin):
    coords = list(parse_line(line))
    for s, e in ((coords[i], coords[i+1]) for i in range(len(coords) - 1)):
        for c in line_coords(s, e):
            grid[c] = "#"

# any sand that get to the level of the lowest rock is gone:
bottom = max(y for (x, y) in grid) + 1
print(simulate(entry, grid, bottom))
