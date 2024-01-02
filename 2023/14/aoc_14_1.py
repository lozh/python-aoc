#!/usr/bin/env python3

import sys
from itertools import product

# input a list of lists
# output (moves, new_layout)
# new_layout is also a list of lists
# currently a destructive update of the input
def move_north(layout):
    height = len(layout)
    width = len(layout[0])
    moves = 0
    for (i, j) in product(range(width), range(1, height)):
        if layout[j][i] == 'O' and layout[j - 1][i] == '.':
            layout[j - 1][i] = 'O'
            layout[j][i] = '.'
            moves += 1

    return (moves, layout)

def load(layout):
    height = len(layout)
    s = 0
    for i, line in enumerate(layout):
        rocks = sum(1 for x in line if x == 'O')
        s += (height - i) * rocks
    return s

lines = map(str.rstrip, sys.stdin)
layout = [list(line) for line in lines]

c, layout = move_north(layout)

while c > 0:
    c, layout = move_north(layout)

print(load(layout))
