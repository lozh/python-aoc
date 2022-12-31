#!/usr/bin/env /usr/bin/python3

import sys
from dataclasses import dataclass

def is_wall(pos, key):
    x, y = pos
    v = x * x + 3 * x + 2 * x * y + y + y * y + key
    return bin(v).count("1") % 2 == 1

def neighbours(pos):
    x, y = pos
    yield x + 1, y
    yield x, y + 1
    if x > 0:
        yield x - 1, y
    if y > 0:
        yield x, y - 1

def distance(pos, target):
    return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

def solve(pos, moves, key):
    visited = set()
    starts = [pos]
    for _ in range(moves + 1):
        new_starts = []
        for n in starts:
            if not is_wall(n, key):
                if not n in visited:
                    visited.add(n)
                    for p in neighbours(n):
                        new_starts.append(p)
        starts = new_starts
    return len(visited)

moves = 50
example_key = 10
puzzle_key = 1352
pos = (1,1)

print(solve(pos, moves, puzzle_key))
