#!/usr/bin/env python3

import sys

# map of input direction, pipe -> output direction
dirs = {
    ('N', '|'): 'N',
    ('S', '|'): 'S',
    ('E', '-'): 'E',
    ('W', '-'): 'W',
    ('S', 'L'): 'E',
    ('W', 'L'): 'N',
    ('S', 'J'): 'W',
    ('E', 'J'): 'N',
    ('N', '7'): 'W',
    ('E', '7'): 'S',
    ('N', 'F'): 'E',
    ('W', 'F'): 'S',
}
# map of start direction, end direction -> start pipe
starts = {
    ('N', 'N'): '|',
    ('N', 'E'): 'J',
    ('N', 'W'): 'L',
    ('E', 'N'): 'F',
    ('E', 'E'): '-',
    ('E', 'S'): 'L',
    ('S', 'E'): '7',
    ('S', 'S'): '|',
    ('S', 'W'): 'F',
    # We don't use 'W' as a start direction, but completing the table
    # helps check for errors
    ('W', 'N'): '7',
    ('W', 'S'): 'J',
    ('W', 'W'): '-',
}

# map of pipe -> 3 x 3 bitmap
pipe_bitmaps = {
    '|': [[False, True, False], [False, True, False], [False, True, False]],
    '-': [[False, False, False], [True, True, True], [False, False, False]],
    'J': [[False, True, False], [True, True, False], [False, False, False]],
    'L': [[False, True, False], [False, True, True], [False, False, False]],
    '7': [[False, False, False], [True, True, False], [False, True, False]],
    'F': [[False, False, False], [False, True, True], [False, True, False]],
}

# lines count from 0 at the north downwards
offsets = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0),
}

fill_offsets = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

def find_start(m):
    for y, line in enumerate(m):
        if 'S' in line:
            return line.index('S'), y
    print("No Start")

def in_bounds(m, x, y):
    return x >= 0 and x < len(m[0]) and y >= 0 and y < len(m)

# This function finds the pipe loop in the map
# It also replaces the start symbol with the correct pipe symbol
def find_loop(m, start):
    for start_dir in ['N', 'E', 'S']:
        x, y = start
        cur_dir = start_dir
        loop = []
        while True:
            loop.append((x, y))
            ox, oy = offsets[cur_dir]
            x = x + ox
            y = y + oy
            if not in_bounds(m, x, y):
                break
            cell = m[y][x]
            if cell == 'S':
                # replace 'S' with pipe shape
                m[y] = m[y][:x] + starts[(start_dir, cur_dir)] + m[y][x + 1:]
                return loop
            if (cur_dir, cell) not in dirs:
                break
            cur_dir = dirs[(cur_dir, cell)]  
    print("No Loop")

# Build a bitmap of the loop
# each cell is a 3 x 3 bitmap
def build_bitmap(m, loop):
    width = len(m[0])
    height = len(m)
    bitmap = [[False for x in range(width * 3)] for y in range(height * 3)]
    for x, y in loop:
        pipe = pipe_bitmaps[m[y][x]]
        for i in range(len(pipe[0])):
            for j in range(len(pipe)):
                bitmap[y * 3 + j][x * 3 + i] = pipe[j][i]
    return bitmap

# If you search from the top left corner
# across and down then the first in the loop
# must be a 'F'. If not it would be connected to something
# higher or to the left, contradicting it being the first
def find_top_left(m, loop):
    for y in range(len(m)):
        for x in range(len(m[0])):
            if (x, y) in loop:
                return x, y

# Flood fill the bit map from the start position
def flood_fill(bitmap, start):
    frontier = {start}
    while frontier:
        new_frontier = set()
        for (x, y) in frontier:
            bitmap[y][x] = True
            fills = ((x + fx, y + fy) for (fx, fy) in fill_offsets)
            for (i, j) in fills:
                if not bitmap[j][i]:
                    new_frontier.add((i, j))
        frontier = new_frontier

    return bitmap

pipemap = list(map(str.rstrip, sys.stdin))
start = find_start(pipemap)
loop = find_loop(pipemap, start)
bitmap = build_bitmap(pipemap, loop)
sx, sy = find_top_left(pipemap, loop)
# We know the top left pipe is a F and that the bottom right is inside the loop
start_fill = (sx * 3 + 2, sy * 3 + 2)
# As we've expanded to 3 x 3 bit maps, we know the interior is contiguous
# So we can find it by flood filling
filled_bitmap = flood_fill(bitmap, start_fill)

# count how many of the centre of the 3 x 3 cells are set
total = sum(1 for x in range(len(pipemap[0])) for y in range(len(pipemap)) if bitmap[y * 3 + 1][x * 3 + 1])
# All the pipe bit maps also have their centre pixel set
print(total - len(loop))
