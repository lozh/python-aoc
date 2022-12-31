#!/usr/bin/env /usr/bin/python3

import sys
from dataclasses import dataclass
from heapq import heappush, heappop

@dataclass(frozen=True)
class State:
    target = (0, 0)
    pos: int
    move_count: int
    def __lt__(self, other):
        d1 = distance(self.pos, self.target) + self.move_count
        d2 = distance(other.pos, other.target) + other.move_count
        return d1 < d2

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

def solve(pos, target, key):
    State.target = target
    visited = set()
    positions = []
    heappush(positions, State(pos = pos, move_count = 0))
    while True:
        n = heappop(positions)
        if n.pos == target:
            return n
        if not n.pos in visited:
            visited.add(n.pos)
            if not is_wall(n.pos, key):
                for p in neighbours(n.pos):
                    heappush(positions, State(pos = p, move_count = n.move_count + 1))

example_target = (7, 4)
puzzle_target = (31, 39)
example_key = 10
puzzle_key = 1352
pos = (1,1)

print(solve(pos, puzzle_target, puzzle_key))
