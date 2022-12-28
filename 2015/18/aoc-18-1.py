#!/usr/bin/env /usr/bin/python3

import sys

def neighbours(x, y, maxx, maxy):
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if x == i and y == j:
                continue
            if i >= 0 and j >= 0 and i < maxx and j < maxy:
                yield i, j

def neighbour_on_count(x, y, maxx, maxy, grid):
    return sum(1 for i, j in neighbours(x, y, maxx, maxy) if grid[j][i])

def parse_line(line):
    yield from (c == "#" for c in line)

def get_initial_grid(lines):
    for line in lines:
        yield list(parse_line(line))

def next_grid(grid, maxx, maxy):
    new_grid = []
    for x in range(maxx):
        line = []
        for y in range(maxy):
            n = neighbour_on_count(x, y, maxx, maxy, grid)
            l = False
            if grid[y][x] and n >= 2 and n <= 3:
                l = True
            if not grid[y][x] and n == 3:
                l = True
            line.append(l)
        new_grid.append(line)
    return new_grid
        
turns = 100

grid = list(get_initial_grid(map(str.rstrip, sys.stdin)))
maxx = len(grid[0])
maxy = len(grid)

for _ in range(turns):
    grid = next_grid(grid, maxx, maxy)

print(sum(1 for line in grid for l in line if l))
