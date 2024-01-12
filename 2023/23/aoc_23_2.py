#!/usr/bin/env python3

import sys
import math
from dataclasses import dataclass
from collections import defaultdict

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
    length: int

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
        return pos.x >= 0 and pos.x < self.width and pos.y >= 0 and pos.y < self.height

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

    # Neat trick stolen from Reddit
    # If you hit the edge, you have divided your map into two
    # You need to move into the part that has the exit
    # This will always be east if you are on the top or bottom
    # Or south is you are on the left or right
    # More preciesely, if you find yourself hitting west on
    # the top or bottom, or north on the left or right
    # then you've gone wrong
    # You should also be able to apply this optimisation
    # To the simplified graph, but it's a bit more difficult
    # Especially to do both
    # Culling here cuts more edges than culling the graph
    def trace_path(self, start: Pos, direction):
        length = 1
        d = direction
        pos = start.neighbour(d)
        prev = start
        while True:
            cell = self[pos]
            match cell:
                case '#':
                    raise ValueError("Shouldn't get here by construction")
                case '.' | '^' | '>' | 'v' | '<':
                    pass
                case _:
                    raise ValueError(f"Unexpected cell value {cell}")

            if self.is_node(pos):
                return Path(start, pos, length)

            for d, p in self.directions(pos):
                # We will only find at most one direction
                # otherwise this would be a node
                if p != prev:
                    prev = pos
                    pos = p
                    length += 1
                    break
            else:
                # Path was a dead-end
                return None

            # See comment at top of function
            # offset by one as the edge is wall
            if (p.x == 1 or p.x == self.width - 2) and d == 'N':
                return None
            if (p.y == 1 or p.y == self.height - 2) and d == 'W':
                return None

    def find_graph(self, start: Pos, direction: str):
        paths = {}
        heads = [(start, direction)]

        while heads:
            pos, direction = heads.pop()
            if path := self.trace_path(pos, direction):
                paths[pos, direction] = path
                for d, _ in self.directions(path.end):
                    if (path.end, d) not in paths:
                        heads.append((path.end, d))
        return paths

def graph_to_dot(paths, start, end):
    node_map = {start: "start", end: "end"}
    n = 'A'
    print("digraph {")
    for path in paths:
        if path.start not in node_map:
            node_map[path.start] = n
            if n == 'Z':
                n = 'a'
            else:
                n = chr(ord(n) + 1)
        if path.end not in node_map:
            node_map[path.end] = n
            if n == 'Z':
                n = 'a'
            else:
                n = chr(ord(n) + 1)
        print(f"\t{node_map[path.start]} -> {node_map[path.end]} [label = {path.length}]")
    print("}")

def longest_path(nodes, edges, start, end):
    def longest_path_r(nodes, edges, start, end, length):
        if start == end:
            return length
        nodes = nodes - {start}
        neighbours = ((pe, pl) for (pe, pl) in edges[start] if pe in nodes)
        return max((longest_path_r(nodes, edges, s, end, length + l) for s, l in neighbours), default = -math.inf)
    return longest_path_r(nodes, edges, start, end, 0)

layout = Layout(list(map(str.rstrip, sys.stdin)))

start = layout.start()
end = layout.end()

# The map is a number of long paths with the occasional choice
# Build up a graph

paths = layout.find_graph(start, 'S')

# With a non directed graph, this is NP-complete
# can't see any shortcut, even though the graph is very regular
# Just brute force
nodes = {path.start for path in paths.values()}.union({path.end for path in paths.values()})

edges = defaultdict(list)
for path in paths.values():
    edges[path.start].append((path.end, path.length))
    
print(longest_path(nodes, edges, start, end))

