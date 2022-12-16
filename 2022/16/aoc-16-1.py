#!/usr/bin/env /usr/bin/python3

import sys
import re
import itertools
from itertools import islice

parse_re = re.compile("^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)$")

class Valve:
    def __init__(self, valve, flow, routes):
        self.valve = valve
        self.flow = flow
        self.routes = routes

    def __str__(self):
        return f"{{valve = {self.valve}, flow = {self.flow}, routes = {self.routes}}}"

class Move:
    def __init__(self, dest):
        self.dest = dest

class TurnValve:
    def __init__(self, valve):
        self.valve = valve

class State:
    # pos is a valve name
    # moves is list of moves taken to get to this position
    # 
    def __init__(self, pos, moves, valves, valves_turned, remaining_mins, score):
        self.pos = pos
        self.moves = moves
        self.valves = valves
        self.valves_turned = valves_turned
        self.remaining_mins = remaining_mins
        self.score = score

    def apply_move(self, move):
        pass

def parse_line(line):
    m = parse_re.match(line)
    if m:
        valve = m.group(1)
        flow = int(m.group(2))
        routes = set(map(str.strip, m.group(3).split(",")))
        return Valve(valve, flow, routes)
    print(f"Couldn't parse line: {line}")
    raise

def max_flow(valves):
    return max(v.flow for v in valves.values())

# return first step to get from src to dest on a shortest path
def path(valves, src, dest):
    len = 0
    visited = {src:None}

    again = True
    while again:
        again = False
        for x in visited.copy():
            valve = valves[x]
            for route in valve.routes:
                if route not in visited:
                    again = True
                    visited[route] = x
                if route == dest:
                    while True:
                        if not visited[visited[route]]:
                            return route
                        route = visited[route]
    # implicitly return None - no path exists


# return hash of (src,dest), next)
# I.e to get from src to dest go to next
def build_paths(valves):
    for src in valves:
        for dest in valves:
            if src != dest:
                yield ((src, dest), path(valves, src, dest))


# our strategy is to pick a next valve to open
# if we're there then open it an then pick another
# if we're not then pick a tunnel that takes us closer
# if we're ever at a valve with more flow than the target
# then abort
def solve(valves, paths, unused, pos, minutes, score, target):
    # We can't score any more if there are no unused valves
    # or we're in the last minute
    if minutes == 0 or not unused:
        yield score
        return

    # We don't have a target, try all unused nodes
    if not target:
        # if we have a disjoint graph, we might not be able to make any more progress
        stuck = True
        for target in unused:
            if paths[(pos, target)]:
                for s in solve(valves, paths, unused, pos, minutes, score, target):
                    yield s
                    stuck = False
        if stuck:
            yield score
    elif pos == target:
        # We're at our target, turn the valve
        flow = valves[pos].flow
        unused.remove(target)
        yield from solve(valves, paths, unused, pos, minutes - 1, score + minutes * flow, None)
        unused.add(target)
    else:
        # We're not at our target
        if valves[pos] in unused and valves[pos].flow >= valves[target].flow:
            # current node is better than where we're trying to go. can't be correct
            return
        else:
            yield from solve(valves, paths, unused, paths[(pos, target)], minutes - 1, score, target)


valves = {x.valve:x for x in map(parse_line, sys.stdin)}
paths = {k:v for k, v in build_paths(valves)}
unused = {k for k, valve in valves.items() if valve.flow > 0}
ans = solve(valves, paths, unused, "AA", 29, 0, None)
print(max(ans))
