#!/usr/bin/env /usr/bin/python3

import sys
import re
from operator import add
from itertools import takewhile, tee, count

def tuple_add(x, y):
    return tuple_map(add, x, y)

# Operate on two tuples by element
def tuple_map(f, x, y):
    return tuple(f(a, b) for (a, b) in zip(x, y))

def cmp(x, y):
    return (x > y) - (x < y)

# This is in itertools in Python 3.10
def pairwise(i):
    a, b = tee(i)
    next(b, None)
    return zip(a, b)

# Returns generator for x, f(x), f(f(x)), ...
# There's a more concise notation for this in Python 3.10
def iterate(f, x):
    while True:
        yield x
        x = f(x)

coord_re = re.compile("^(\d+),(\d+)$")
def parse_line(line):
    for coord in str.split(line, " -> "):
        m = coord_re.match(coord)
        yield int(m.group(1)), int(m.group(2))

def line_coords(start, end):
    # Direction of the line to move from start to end
    offset = tuple_map(cmp, end, start)
    add_offset = lambda pos: tuple_add(pos, offset)
    projection = iterate(add_offset, start)
    yield from takewhile(lambda pos: pos != end, projection)
    yield end

# Build grid. Just a map of (x, y) -> symbol
def parse_rocks(lines):
    for line in lines:
        coords = parse_line(line)
        for s, e in pairwise(coords):
            yield from line_coords(s, e)

# Returns the next position for sand falling
# Same as input if it doesn't move
def sand_next_pos(pos, grid):
    # possible routes down    
    offsets = [(0, 1), (-1, 1), (1, 1)]
    for offset in offsets:
        new_pos = tuple_add(pos, offset)
        if new_pos not in grid:
            return new_pos
    return pos

# Returns the position sand ends up in, None if it escapes
def sand(start, grid, bottom):
    while True:
        pos = sand_next_pos(start, grid)
        if pos == start:
            return pos
        if pos[1] >= bottom:
            return None
        start = pos

# Run the simulation
def simulate(entry, grid, bottom):
    for i in count():
        s = sand(entry, grid, bottom)
        if not s:
            # sand escaped
            return i
        grid.add(s)

# where sand enters from
entry = (500, 0)
grid = {x for x in parse_rocks(map(str.rstrip, sys.stdin))}

# Any sand that get to the level of the lowest rock is gone:
bottom = max(y for (x, y) in grid)
print(simulate(entry, grid, bottom))
