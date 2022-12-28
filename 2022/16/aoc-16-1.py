#!/usr/bin/env /usr/bin/python3

import sys
import re

parse_re = re.compile("^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)$")

class Valve:
    def __init__(self, valve, flow, routes):
        self.valve = valve
        self.flow = flow
        self.routes = routes

    def __str__(self):
        return f"{{valve = {self.valve}, flow = {self.flow}, routes = {self.routes}}}"

def parse_line(line):
    m = parse_re.match(line)
    if m:
        valve = m.group(1)
        flow = int(m.group(2))
        routes = set(map(str.strip, m.group(3).split(",")))
        return Valve(valve, flow, routes)
    print(f"Couldn't parse line: {line}")
    raise

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
    # We're assuming the graph is connected
    raise

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
        for target in unused:
            yield from solve(valves, paths, unused, pos, minutes, score, target)
    elif pos == target:
        # We're at our target, turn the valve
        flow = valves[pos].flow
        unused.remove(target)
        yield from solve(valves, paths, unused, pos, minutes - 1, score + minutes * flow, None)
        unused.add(target)
    else:
        # We're not at our target
        yield from solve(valves, paths, unused, paths[(pos, target)], minutes - 1, score, target)

valves = {x.valve:x for x in map(parse_line, sys.stdin)}
paths = {k:v for k, v in build_paths(valves)}
unused = {k for k, valve in valves.items() if valve.flow > 0}
ans = solve(valves, paths, unused, "AA", 29, 0, None)
print(max(ans))
