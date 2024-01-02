#!/usr/bin/env python3

import sys
from itertools import product

# input a list of lists
# output (moves, new_layout)
# new_layout is also a list of lists
# currently a destructive update of the input
def move_north(layout, height, width):
    c = 0
    for (i, j) in product(range(width), range(1, height)):
        if layout[j][i] == 'O' and layout[j - 1][i] == '.':
            layout[j - 1][i] = 'O'
            layout[j][i] = '.'
            c += 1

    return c, layout

def move_east(layout, height, width):
    c = 0
    for (i, j) in product(range(width - 1), range(height)):
        if layout[j][i] == 'O' and layout[j][i + 1] == '.':
            layout[j][i + 1] = 'O'
            layout[j][i] = '.'
            c += 1
            
    return c, layout

def move_south(layout, height, width):
    c = 0
    for (i, j) in product(range(width), range(height - 1)):
        if layout[j][i] == 'O' and layout[j + 1][i] == '.':
            layout[j + 1][i] = 'O'
            layout[j][i] = '.'
            c += 1

    return c, layout

def move_west(layout, height, width):
    c = 0
    for (i, j) in product(range(1, width), range(height)):
        if layout[j][i] == 'O' and layout[j][i - 1] == '.':
            layout[j][i - 1] = 'O'
            layout[j][i] = '.'
            c += 1

    return c, layout

def load(layout, height):
    s = 0
    for i, line in enumerate(layout):
        rocks = sum(1 for x in line if x == 'O')
        s += (height - i) * rocks
    return s

lines = map(str.rstrip, sys.stdin)
layout = [list(line) for line in lines]
height = len(layout)
width = len(layout[0])

layout_map = {}
layout_list = []
rounds = 1000000000

for x in range(rounds):
    m = 1
    while m > 0:
        m, layout = move_north(layout, height, width)

    m = 1
    while m > 0:
        m, layout = move_west(layout, height, width)
        
    m = 1
    while m > 0:
        m, layout = move_south(layout, height, width)

    m = 1
    while m > 0:
        m, layout = move_east(layout, height, width)

    layout_key = tuple(map(tuple, layout))

    # look for the start of a cycle
    if layout_key in layout_map:
        c = layout_map[layout_key]
        cycle = x - c
        # -1 because we're counting from 0
        n = c + (rounds - 1 - c) % cycle
        print(load(layout_list[n], height))
        break

    layout_map[layout_key] = x
    layout_list.append(layout_key)
    
