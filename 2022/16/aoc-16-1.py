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

def solve(valves, pos, minutes, src, max_flow_left, score):
    # depth first search of solution space
    # if we've run out of time, or we've turned all the valves
    # we can't score any more
    if minutes == 1 or max_flow_left == 0:
        yield score
        return

    valve = valves[pos]
    check_tunnels = True

    # go through each possible move first can we turn the current valve
    if valve.flow > 0:
        flow = valve.flow
        valve.flow = 0
        new_max_flow = max_flow(valves)
        # don't check tunnels if this is the highest flow left
        check_tunnels = flow != max_flow_left
        yield from solve(valves, pos, minutes - 1,  None, new_max_flow, score + (minutes - 1) * flow)
        valve.flow = flow

    # now go through possible tunnel moves
    if minutes > 2 and check_tunnels:
        for dest in (dest for dest in valve.routes if dest != src):
            yield from solve(valves, dest, minutes - 1, pos, max_flow_left, score)
    
valves = {x.valve:x for x in map(parse_line, sys.stdin)}
max_flow_left = max_flow(valves)

ans = max(solve(valves, "AA", 30, None, max_flow_left, 0))
print(ans)
#result = islice(solve(valves, "AA", 30, valves_turned, None, 0), 1000000, 1000010)
#print(list(result))
