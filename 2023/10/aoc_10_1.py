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

# lines count from 0 at the north downwards
offsets = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0),
}

def find_start(m):
    for y, line in enumerate(m):
        if 'S' in line:
            return line.index('S'), y
def in_bounds(m, x, y):
    return x >= 0 and x < len(m[0]) and y >= 0 and y < len(m)

def find_loop_size(m, start):
    for start_dir in ['N', 'E', 'S']:
        size = 0
        x, y = start
        cur_dir = start_dir
        while True:
            size += 1
            ox, oy = offsets[cur_dir]
            x = x + ox
            y = y + oy
            if not in_bounds(m, x, y):
                break
            cell = m[y][x]
            if cell == 'S':
                return size
            if (cur_dir, cell) not in dirs:
                break
            cur_dir = dirs[(cur_dir, cell)]  
    print("No Loop")
            
        
pipemap = list(map(str.rstrip, sys.stdin))

start = find_start(pipemap)

size = find_loop_size(pipemap, start)

print (int(size / 2))

    
