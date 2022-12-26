#!/usr/bin/env /usr/bin/python3

import sys
import re
from dataclasses import dataclass
from time import sleep

@dataclass
class ResourceSpec:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other):
        return ResourceSpec(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode
        )

    def __sub__(self, other):
        return ResourceSpec(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode
        )

    def can_spend(self, other):
        return self.ore >= other.ore and self.clay >= other.clay and self.obsidian >= other.obsidian and self.geode >= other.geode

@dataclass
class Blueprint:
    id: int
    ore_robot: ResourceSpec
    clay_robot: ResourceSpec
    obsidian_robot: ResourceSpec
    geode_robot: ResourceSpec

@dataclass
class State:
    resources: ResourceSpec
    robots: ResourceSpec

blueprint_re = re.compile("^Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.$")

def parse_blueprint(line):
    m = blueprint_re.match(line)
    return Blueprint(
        id = int(m.group(1)),
        ore_robot = ResourceSpec(ore = int(m.group(2))),
        clay_robot = ResourceSpec(ore = int(m.group(3))),
        obsidian_robot = ResourceSpec(ore = int(m.group(4)), clay = int(m.group(5))),
        geode_robot = ResourceSpec(ore = int(m.group(6)), obsidian = int(m.group(7)))
    )

one_geode_robot = ResourceSpec(geode = 1)
one_obsidian_robot = ResourceSpec(obsidian = 1)
one_ore_robot = ResourceSpec(ore = 1)
one_clay_robot = ResourceSpec(clay = 1)

max_geodes = 0

# imagine we could create a new geode robot every turn from here
# how many geodes would we end up with
def max_geode_from(current, robots, minutes):
    return current + robots * minutes + (minutes * (minutes - 1) >> 1)
    
def goals(blueprint, state):
    # what could we aim to build next
    if state.robots.obsidian > 0:
        yield blueprint.geode_robot, one_geode_robot
    if state.robots.clay > 0:
        yield blueprint.obsidian_robot, one_obsidian_robot
    yield blueprint.clay_robot, one_clay_robot
    yield blueprint.ore_robot, one_ore_robot

def simulate(blueprint, state, goal, minutes):
    global max_geodes
    if minutes == 0:
        if state.resources.geode >= max_geodes:
            max_geodes = state.resources.geode
            # yield state
            yield state.resources.geode
    else:
        if max_geode_from(state.resources.geode, state.robots.geode, minutes) < max_geodes:
            return
        if goal == None:
            for g in goals(blueprint, state):
                yield from simulate(blueprint, state, g, minutes)
        else:
            cost, produce = goal
            resources = state.resources
            robots = state.robots
            if resources.can_spend(cost):
                # each robot produces one resource
                resources += robots
                robots += produce
                resources -= cost
                goal = None
            else:
                # each robot produces one resource
                resources += robots

            yield from simulate(blueprint, State(resources, robots), goal, minutes - 1)

def solve(blueprint, initial_state, minutes):
    return max(simulate(blueprint, initial_state, None, minutes), default = 0)

def solve_blueprints(blueprints, minutes):
    global max_geodes
    for blueprint in blueprints:
        initial_state = State(
            resources = ResourceSpec(),
            robots = ResourceSpec(ore = 1)
        )
        max_geodes = 0
        score = solve(blueprint, initial_state, minutes)
        yield blueprint.id, score
        # cool down CPU
        sleep(2)
        
    

blueprints = map(parse_blueprint, sys.stdin)

minutes = 24

total = 0

for id, score in solve_blueprints(blueprints, minutes):
    print(f"{id}, {score}")
    total += id * score

print(total)
    
