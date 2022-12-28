#!/usr/bin/env /usr/bin/python3

import sys
from dataclasses import dataclass
from heapq import heappush, heappop

blizzard_syms = {'>', '^', 'v', '<'}

@dataclass(frozen=True)
class Pos:
    x: int
    y: int
    t: int
    target_x = 0
    target_y = 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    # Finding the shortest path depends on this ordering
    # Always ordering shorter paths before longer ones
    def __cmp__(self, other):
        a = self.__key__()
        b = other.__key__()
        if a != b:
            return (a > b) - (a < b)
        else:
            # prefer more evolved positions
            return (self.t < other.t) - (self.t > other.t)

    def __key__(self):
        return abs(self.x - self.target_x) + abs(self.y - self.target_y) + self.t

def parse_input(lines):
    # treat the board as 0,0 at the top corner inside the walls
    # we start at y = -1 outside
    line = next(lines)
    start = (line.index('.') - 1, -1)
    width = len(line) - 2
    blizzards = set()
    for y, line in enumerate(lines):
        for x, b in enumerate(line):
            if b in blizzard_syms:
                # x - 1 to skip the initial wall
                blizzards.add((x - 1, y, b))
    end = (line.index('.') - 1, y)
    height = y
    return start, end, width, height, blizzards

def blizzard_at_pos_at_t(blizzards, x, y, t, width, height):
    # there are only 4 places a blizzard could start from to be at any given pos at time t.
    return ((x - t) % width, y, '>') in blizzards or ((x + t) % width, y, '<') in blizzards or (x, (y - t) % height, 'v') in blizzards or (x, (y + t) % height, '^') in blizzards

def moves(start, end, width, height, x, y):
    # special case for start and end
    if y == height - 1 and x == end[0]:
        yield end

    if y < height - 1:
        yield (x, y + 1)

    if x < width - 1 and y >= 0:
        yield (x + 1, y)

    # do nothing
    yield (x, y)

    if y > 0:
        yield (x, y - 1)

    if x > 0 and y < height:
        yield (x - 1, y)

    if y == 0 and x == start[0]:
        yield start

def solve(start, end, width, height, blizzards, start_t):
    visited = set()
    heap = []
    Pos.target_x = end[0]
    Pos.target_y = end[1]
    heappush(heap, Pos(x = start[0], y = start[1], t = start_t))
    while True:
        pos = heappop(heap)
        if pos not in visited:
            visited.add(pos)
            if (pos.x, pos.y) == end:
                return pos.t
            for x, y in moves(start, end, width, height, pos.x, pos.y):
                if not blizzard_at_pos_at_t(blizzards, x, y, pos.t + 1, width, height):
                    heappush(heap, Pos(x = x, y = y, t = pos.t + 1))

start, end, width, height, blizzards = parse_input(map(str.rstrip, sys.stdin))

t = solve(start, end, width, height, blizzards, 0)
t = solve(end, start, width, height, blizzards, t)
t = solve(start, end, width, height, blizzards, t)

print(t)
