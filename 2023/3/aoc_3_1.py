#!/usr/bin/env python3

import sys
import re

def is_symbol(c):
    m = re.match("[0-9.]", c)
    return m is None

def scan_line_for_numbers(i, line):
    start = 0
    while True:
        m = re.search(r"(\d+)", line[start:])
        if m:
            yield (int(m[0]), start + m.start(0), i, m.end(0) - m.start(0))
            start = start + m.end(0)
        else:
            break

# scan the grid, output (number, x, y, len)
def scan_for_numbers(grid):
    for (x, line) in enumerate(grid):
        yield from scan_line_for_numbers(x, line)

def is_in_bounds(x, y, bounds):
    minx, miny, maxx, maxy = bounds
    return x >= minx and x < maxx and y >= miny and y < maxy

def adjacent_cells(x, y, bounds):
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i != 0 or j != 0) and is_in_bounds(x + i, y + j, bounds):
                yield (x + i, y + j)

def is_symbol_adjacent_to_cell(x, y, grid, bounds):
    return any(is_symbol(grid[j][i]) for (i, j) in adjacent_cells(x, y, bounds))
        
def is_symbol_adjacent_to_number(number, grid, bounds):
    n, x, y, l = number
    r = any(is_symbol_adjacent_to_cell(i, y, grid, bounds) for i in range(x, x + l))
    #print(f"{number}, {r}")
    return r
    
def scan_for_part_numbers(grid, bounds):
    numbers = scan_for_numbers(grid)
    part_numbers = (n[0] for n in numbers if is_symbol_adjacent_to_number(n, grid, bounds))
    yield from part_numbers

stdin = map(str.rstrip, sys.stdin)
grid = list(stdin)
# minx, miny, maxx, maxy
bounds = (0, 0, len(grid[0]), len(grid))
print(sum(scan_for_part_numbers(grid, bounds)))
