#!/usr/bin/env /usr/bin/python3

import sys
import re
from dataclasses import dataclass
from copy import copy

parse_re = re.compile("^/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%$")

@dataclass(frozen=True)
class Node:
    size: int
    used: int
    avail: int

def neighbours(pos, max_x, max_y):
    x, y = pos
    if x > 0:
        yield x - 1, y
    if x < max_x:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < max_y:
        yield x, y + 1

@dataclass(frozen=True)
class State:
    max_x = 0
    max_y = 0
    # (x, y) -> Node
    nodes: dict
    move_count: int
    # where is the data we're trying to exfiltrate
    data_pos: tuple
    # where is the empty square, this stops this being a general solution
    empty_pos: tuple

    def is_complete(self):
        return (0, 0) == self.data_pos

    # Find the shortest sequence of moves to get the empty_pos to dest
    def path(self, dest):
        visited = {self.empty_pos: []}
        frontier = {self.empty_pos}
        while True:
            new_frontier = set()
            for f in frontier:
                nf = self.nodes[f]
                if f == dest:
                    return visited[f]
                for t in neighbours(f, State.max_x, State.max_y):
                    if t not in visited and t != self.data_pos:
                        nt = self.nodes[t]
                        if nt.used <= nf.size:
                            visited[t] = visited[f] + [t]
                            new_frontier.add(t)
            if not new_frontier:
                raise Exception("No Path Found")
            frontier = new_frontier

    # apply a move and return a new state
    def move(self, src, dst):
        nodes = copy(self.nodes)
        f = nodes[src]
        t = nodes[dst]
        nodes[dst] = Node(size = t.size, used = t.used + f.used, avail = t.avail - f.used)
        nodes[src] = Node(size = f.size, used = 0, avail = f.size)
        return State (
            nodes = nodes,
            move_count = self.move_count + 1,
            data_pos = dst if self.data_pos == src else self.data_pos,
            empty_pos = src
        )

    def __str__(self):
        disp = [f"{self.empty_pos}, {self.data_pos}\n"]
        for y in range(State.max_y + 1):
            for x in range(State.max_x + 1):
                n = self.nodes[(x, y)]
                if n.used == 0:
                    disp.append("_")
                elif n.size > 500:
                    disp.append("#")
                elif (x, y) == self.data_pos:
                    disp.append("G")
                else:
                    disp.append(".")
            disp.append("\n")
        return "".join(disp)

def parse_line(line):
    if m := parse_re.match(line):
        return int(m.group(1)), int(m.group(2)), Node(
            size = int(m.group(3)),
            used = int(m.group(4)),
            avail = int(m.group(5)),
        )
    else:
        raise Exception(f"Could not parse line {line}")

# This is very much based on the specific problem
# It isn't a general solution to any layout
# Basically there is one gap we can move around
# And the solution is to repeatedly move it to the left of the
# data we want to exfiltrate without crossing over the data cell
# Need to avoid blocked cells which have too much data to be
# feasible to ever move
def solve(initial):
    s = initial
    while True:
        if s.is_complete():
            return s
        dest = (s.data_pos[0] - 1, s.data_pos[1])
        for m in s.path(dest):
            s = s.move(m, s.empty_pos)
        s = s.move(s.data_pos, s.empty_pos)

inp = sys.stdin
_ = next(inp)
_ = next(inp)

nodes = {}

for x, y, n in map(parse_line, inp):
    nodes[(x, y)] = n
    if n.used == 0:
        empty_pos = (x, y)

State.max_x = max(x for (x, _) in nodes)
State.max_y = max(y for (_, y) in nodes)

data_pos = (State.max_x, 0)

initial = State (
    nodes = nodes,
    move_count = 0,
    data_pos = data_pos,
    empty_pos = empty_pos
)
s = solve(initial)
print(s.move_count)
