#!/usr/bin/env python3

import sys
from dataclasses import dataclass

class Layout:
    cells: list[str]
    width: int
    height: int

    def __init__(self, cells):
        self.cells = list(cells)
        self.width = len(self.cells[0])
        self.height = len(self.cells)

    def start(self):
        for y in range(self.height):
            if 'S' in self.cells[y]:
                return self.cells[y].index('S'), y
        raise ValueError("Could not find Start")

    def in_bounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def is_garden(self, x, y):
        return self.in_bounds(x, y) and self.cells[y][x] != '#'

    def open_neighbours(self, pos):
        x, y = pos
        for (i, j) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if self.is_garden(x + i, y + j):
                yield x + i, y + j

def expand_frontier(layout, frontier):
    new_frontier = set()
    for pos in frontier:
        new_frontier.update(layout.open_neighbours(pos))
    return new_frontier

layout = Layout(map(str.rstrip, sys.stdin))
start = layout.start()
frontier = {start}

for _ in range(64):
    frontier = expand_frontier(layout, frontier)

print(len(frontier))
