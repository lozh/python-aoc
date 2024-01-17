#!/usr/bin/env python3

import sys
import re
from functools import reduce
from operator import mul

def is_gear(c):
    return c == '*'

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

def adjacent_cells(x, y, xlen, bounds):
    for i in range(-1, xlen + 1):
        for j in [-1, 0, 1]:
            if (i < 0 or i >= xlen or j != 0) and is_in_bounds(x + i, y + j, bounds):
                yield (x + i, y + j)

def get_adjacent_gear_positions(number, grid, bounds):
    n, x, y, l = number
    ag = (((i, j), number[0]) for (i, j) in adjacent_cells(x, y, l, bounds) if is_gear(grid[j][i]))
    yield from ag

def nums_to_gear_positions(numbers, grid, bounds):
    yield from (get_adjacent_gear_positions(number, grid, bounds) for number in numbers)
    
def collate_gears(gear_positions):
    r = {}
    # not quite sure how I've got an extra level of indirection here
    for x in gear_positions:
        for (gear_pos, number) in x:
            if gear_pos in r:
                r[gear_pos].append(number)
            else:
                r[gear_pos] = [number]
    return r

def score_gears(gears):
    for _, num_list in gears.items():
        if len(num_list) == 2:
            yield reduce(mul, num_list, 1)

stdin = map(str.rstrip, sys.stdin)
grid = list(stdin)
# minx, miny, maxx, maxy
bounds = (0, 0, len(grid[0]), len(grid))
numbers = scan_for_numbers(grid)
gear_positions = nums_to_gear_positions(numbers, grid, bounds)
gears = collate_gears(gear_positions)

print(sum(score_gears(gears)))
