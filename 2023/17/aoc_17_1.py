#!/usr/bin/env python3
import sys
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from heapq import heappush, heappop

class Direction(Enum):
    NONE = auto()
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    def possible(self):
        if self != Direction.NORTH:
            yield Direction.SOUTH
        if self != Direction.WEST:
            yield Direction.EAST
        if self != Direction.SOUTH:
            yield Direction.NORTH
        if self != Direction.EAST:
            yield Direction.WEST

@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def next(self, direction: Direction):
        x, y = self.x, self.y
        match direction:
            case Direction.NORTH:
                return Pos(x, y - 1)
            case Direction.EAST:
                return Pos(x + 1, y)
            case Direction.SOUTH:
                return Pos(x, y + 1)
            case Direction.WEST:
                return Pos(x - 1, y)

    def in_bounds(self, width: int, height: int):
        return self.x >= 0 and self.x < width and self.y >= 0 and self.y < height

    def is_possible(self, direction: Direction, width, height):
        if direction == Direction.NONE:
            return False
        if self.x == 0 and direction == Direction.EAST:
            return False
        if self.y == 0 and direction == Direction.SOUTH:
            return False
        if self.x == width - 1 and direction == Direction.WEST:
            return False
        if self.y == height - 1 and direction == Direction.NORTH:
            return False
        return True

@dataclass(frozen=True)
class Layout:
    cells: list[list[int]]

    def __init__(self, lines):
        object.__setattr__(self, "cells", [list(map(int, x)) for x in lines])

    def width(self):
        return len(self.cells[0])

    def height(self):
        return len(self.cells)

    def __getitem__(self, key):
        return self.cells[key.y][key.x]

    def __str__(self):
        def strlines():
            for line in self.cells:
                yield ''.join(map(str, line))
        return '\n'.join(strlines())

@dataclass(frozen=True)
class Vertex:
    pos: Pos
    direction: Direction
    consecutive: int

    def move(self, direction: Direction):
        consecutive = self.consecutive + 1 if self.direction == direction else 0
        pos = self.pos.next(direction)
        return Vertex(pos, direction, consecutive)

    def neighbours(self, width, height):
        for d in self.direction.possible():
            n = self.move(d)
            if n.pos.in_bounds(width, height) and n.consecutive <= 2:
                yield n

    def __lt__(self, other):
        return False

@dataclass(order=True)
class Priority:
    priority: int
    item: Vertex = field(compare=False)

# treat as a minimum path problem, but with an exploded definition of vertices
# to include the direciton and consecutive moves in that direction
# solve with Dijkstra
def min_heat_loss(start, end, vertices, layout):
    dist = {}
    q = []
    # as per Python docs to allow us to change the priority of something in the queue
    entry_finder = {}

    for v in vertices:
        dist[v] = 0 if v == start else math.inf
        entry = Priority(dist[v], v)
        entry_finder[v] = entry
        heappush(q, entry)

    while q:
        u = heappop(q).item

        if not u:
            # ignore tombstones
            continue

        del entry_finder[u]
        for v in u.neighbours(width, height):
            alt = dist[u] + layout[v.pos]
            if alt < dist[v]:
                dist[v] = alt
                # replace priority by tombstoning existing priority
                entry = entry_finder.pop(v)
                entry.item = None
                entry = Priority(alt, v)
                entry_finder[v] = entry
                heappush(q, entry)

    return min(d for k, d in dist.items() if k.pos == end)

layout = Layout(map(str.rstrip, sys.stdin))
width, height = layout.width(), layout.height()
end = Pos(width - 1, height - 1)

start = Vertex(Pos(0, 0), Direction.NONE, 0)
vertices = [start]

for p in (Pos(i, j) for i in range(width) for j in range(height)):
    for d in (d for d in Direction if p.is_possible(d, width, height)):
        for c in range(3):
            vertices.append(Vertex(p, d, c))

print(min_heat_loss(start, end, vertices, layout))
