#!/usr/bin/env python3

import sys
from dataclasses import dataclass

directions = "NESW"

slope_map = {
    'N': '^',
    'E': '>',
    'S': 'v',
    'W': '<',
}
direction_map = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}

opposite_map = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E',
}

@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def neighbours(self):
        yield from (self.neighbour(d) for d in directions)

    def neighbour(self, direction):
        x, y = direction_map[direction]
        return Pos(self.x + x, self.y + y)

@dataclass
class Path:
    start: Pos
    end: Pos
    start_dir: str
    end_dir: str
    length: int
    forward: bool
    backward: bool

@dataclass
class Layout:
    cells: list[str]
    height: int
    width: int

    def __init__(self, cells):
        self.cells = cells
        self.height = len(cells)
        self.width = len(cells[0])

    def in_bounds(self, pos: Pos):
        return pos.x >= 0 and pos.x < self.width - 1 and pos.y >= 0 and pos.y < self.height - 1

    def directions(self, pos: Pos):
        for d in directions:
            n = pos.neighbour(d)
            if self.in_bounds(n) and self[n] != '#':
                yield d, n

    def __getitem__(self, key: Pos):
        return self.cells[key.y][key.x]

    def start(self):
        return Pos(self.cells[0].index('.'), 0)

    def end(self):
        return Pos(self.cells[-1].index('.'), self.height - 1)

    def is_node(self, pos: Pos):
        return pos == self.start() or pos == self.end() or len(list(self.directions(pos))) > 2

    def trace_path(self, start: Pos, direction):
        # can we follow this path forward?
        forward = True
        # can wer follow this path backward?
        backward = True
        length = 1
        start_dir = direction
        d = direction
        pos = start.neighbour(d)
        prev = start
        while True:
            cell = self[pos]
            match cell:
                case '#':
                    raise ValueError("Shouldn't get here by construction")
                case '.':
                    pass
                case '^' | '>' | 'v' | '<':
                    if cell == slope_map[d]:
                        backward = False
                    else:
                        forward = False
            if not forward and not backward:
                return None
            if self.is_node(pos):
                return Path(start, pos, start_dir, d, length, forward, backward)
            for d, p in self.directions(pos):
                if p != prev:
                    prev = pos
                    pos = p
                    length += 1
                    break
            else:
                # Path was a dead-end
                return None

layout = Layout(list(map(str.rstrip, sys.stdin)))

start = layout.start()
end = layout.end()

# The map is a number of long paths with the occasional choice
# Built up a directed weighted graph

paths = {}
heads = [(start, 'S')]

while heads:
    pos, direction = heads.pop()
    if path := layout.trace_path(pos, direction):
        paths[pos, direction] = path
        for d, _ in layout.directions(path.end):
            if (path.end, d) not in paths:
                heads.append((path.end, d))

print(paths)
