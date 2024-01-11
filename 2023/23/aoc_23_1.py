#!/usr/bin/env python3

import sys
import math
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
                case '.':
                    pass
                case '^' | '>' | 'v' | '<':
                    if cell != slope_map[d]:
                        return None

            if self.is_node(pos):
                # -length so we can solve DAG by Bellman Ford
                return Path(start, pos, -length)

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

# need an algorithm that works with negative edge weights
def bellman_ford(nodes, edges, start, end):
    dist = {}
    prev = {}

    for v in nodes:
        dist[v] = 0 if v == start else math.inf
        prev[v] = None

    for _ in range(len(nodes) - 1):
        for edge in edges:
            u, v, w = edge.start, edge.end, edge.length
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    return dist[end]


layout = Layout(list(map(str.rstrip, sys.stdin)))

start = layout.start()
end = layout.end()

# The map is a number of long paths with the occasional choice
# Built up a directed weighted graph

paths = layout.find_graph(start, 'S')

# by inspection, the derived graph is a DAG
# in which case we can solve by finding the shortest distance
# for the negative weights.

nodes = {path.start for path in paths.values()}.union({path.end for path in paths.values()})
edges = list(paths.values())
print(-bellman_ford(nodes, edges, start, end))
