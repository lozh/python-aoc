#!/usr/bin/env /usr/bin/python3

import sys
from collections import namedtuple
from heapq import heappush, heappop
from dataclasses import dataclass
from hashlib import md5

Point = namedtuple("Point", ["x", "y"])

max_x = 3
max_y = 3

goal = Point(max_x, max_y)

@dataclass(frozen=True)
class State:
    pos: Point
    move_count: int
    moves: str

    def __lt__(self, other):
        s1 = dist(self.pos, goal) + self.move_count
        s2 = dist(other.pos, goal) + other.move_count
        if s1 == s2:
            return self.moves < other.moves
        else:
            return s1 < s2

def dist(pos1, pos2):
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

def neighbours(pos, h):
    if pos.x > 0 and h[0] in "bcdef":
        yield Point(pos.x - 1, pos.y), 'U'
    if pos.x < 3 and h[1] in "bcdef":
        yield Point(pos.x + 1, pos.y), 'D'
    if pos.y > 0 and h[2] in "bcdef":
        yield Point(pos.x, pos.y - 1), 'L'
    if pos.y < 3 and h[3] in "bcdef":
        yield Point(pos.x, pos.y + 1), 'R'

def is_finished(pos):
    return pos == goal

def solve(key):
    start = State(pos = Point(0, 0), move_count = 0, moves = "")
    heap = []
    heappush(heap, start)
    while s:= heappop(heap):
        if is_finished(s.pos):
            return s
        h = md5((key + s.moves).encode()).digest().hex()
        for n, d in neighbours(s.pos, h):
            heappush(heap, State(pos = n, move_count = s.move_count + 1, moves = s.moves + d))

key = sys.stdin.readline().strip()
print(solve(key))
