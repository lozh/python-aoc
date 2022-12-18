#!/usr/bin/env /usr/bin/python3

import sys
import itertools
from itertools import cycle

shapes = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)]
]

offsets = { '>':(1, 0), '<':(-1, 0) }
down = (0, -1)

def height(shape):
    return max(y for _, y in shape) + 1

def add_pair(x, y):
    return (x[0] + y[0], x[1] + y[1])

def can_move(rock, pos, offset, world):
    for r in rock:
        x, y = add_pair(add_pair(pos, r), offset)
        if x < 0:
            return False
        if x > 6:
            return False
        if y < 0:
            return False
        if (x, y) in world:
            return False
    return True

world = set()

input = sys.stdin.readline().strip()

rock_count = 2022

rocks = cycle(shapes)
input = cycle(iter(input))

top = 0

for rock_no in range(rock_count):
    rock = next(rocks)
    pos = (2, top + 3)
    # simulate rock
    while True:
        # apply jet
        jet = next(input)
        offset = offsets[jet]
        if can_move(rock, pos, offset, world):
            pos = add_pair(pos, offset)
        if can_move(rock, pos, down, world):
            pos = add_pair(pos, down)
        else:
            break
    # Add rock to world
    for r in rock:
        world.add(add_pair(pos, r))
    if pos[0] == -1:
        break
    top = max(top, pos[1] + height(rock))

print(top)
    
