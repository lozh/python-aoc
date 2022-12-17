#!/usr/bin/env /usr/bin/python3

import sys
import re
import itertools
from itertools import product
import copy
from copy import copy

parse_re = re.compile("^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)$")

class Valve:
    def __init__(self, valve, flow, routes):
        self.valve = valve
        self.flow = flow
        self.routes = routes

    def __str__(self):
        return f"{{valve = {self.valve}, flow = {self.flow}, routes = {self.routes}}}"

    def __repr__(self):
        return self.__str__()

# Someone in the tunnel system heading to a target
class Actor:
    def __init__(self, id, pos, target):
        self.id = id
        self.pos = pos
        self.target = target

    def __str__(self):
        return f"{{id = {self.id}, pos = {self.pos}, target = {self.target}}}"

    def __repr__(self):
        return self.__str__()
    
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
    # implicitly return None - no path exists


# return hash of (src,dest), next)
# I.e to get from src to dest go to next
def build_paths(valves):
    for src in valves:
        for dest in valves:
            if src != dest:
                yield ((src, dest), path(valves, src, dest))

# List of all next actor strategies to use
def actor_strategy(paths, unused, actor, actors, tab):
    if actor.target:
        # print(f"{tab}actor_strategy target: {actor}")
        yield actor
    else:
        have_targets = False
        for target in unused:
            if target not in (actor.target for actor in actors):
                if paths[(actor.pos, target)]:
                    a = Actor(actor.id, actor.pos, target)
                    # print(f"{tab}actor_strategy new target: {a}")
                    yield a
                    have_targets = True
        if not have_targets:
            # because we're using cross product, need to supply something
            # print(f"{tab}actor_strategy none available: {actor}")
            yield actor

def actors_strategy(paths, unused, actors, tab):
    # print(f"{tab}actors_strategy({unused}, {actors})")
    x = map(lambda actor: actor_strategy(paths, unused, actor, actors, tab), actors)
    return product(*x)
    
# our strategy is to pick a next valve to open
# if we're there then open it an then pick another
# if we're not then pick a tunnel that takes us closer
# if we're ever at a valve with more flow than the target
# then abort
def solve(valves, paths, unused, actors, minutes, score):
    tab = (25 - minutes) * ' '
    # print(f"{tab}solve({unused}, {actors}, {minutes}, {score})")
    # We can't score any more if there are no unused valves
    # or we're in the last minute
    if minutes == 0 or not unused:
        # print(f"{tab}solve: yield score = {score}, {minutes}, {unused}")
        yield score
        return

    for new_actors in actors_strategy(paths, unused, actors, tab):
        # print(f"{tab}solve 1: new_actors: {unused}, {actors}, {minutes}, {score}")
        new_actors = list(map(lambda actor: copy(actor),new_actors))
        targets = [actor.target for actor in new_actors if actor.target]
        if len(set(targets)) != len(targets):
            # strategy has given same target to both actors
            # print(f"BROKEN STRATEGY")
            continue
        used = set()
        extra_score = 0
        for actor in new_actors:
            # print(f"{tab}solve 2: {actor}, {unused}, {minutes}, {score}")
            if actor.pos == actor.target and actor.target:
                flow = valves[actor.pos].flow
                actor.target = None
                extra_score += minutes * flow
                used.add(actor.pos)
                # print(f"{tab}solve 3: {actor}, {used}, {minutes}, {score}")
            elif actor.target != None:
                actor.pos = paths[(actor.pos, actor.target)]
        yield from solve(valves, paths, unused - used, new_actors, minutes - 1, score + extra_score)
        # print(f"{tab}solve 5: yield: {unused}, {minutes}, {score}")

valves = {x.valve:x for x in map(parse_line, sys.stdin)}
paths = {k:v for k, v in build_paths(valves)}
unused = {k for k, valve in valves.items() if valve.flow > 0}
actors = [Actor(0, "AA", None), Actor(1, "AA", None)]
ans = solve(valves, paths, unused, actors, 25, 0)
print(max(ans))
