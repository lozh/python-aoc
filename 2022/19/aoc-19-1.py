#!/usr/bin/env /usr/bin/python3

import sys
import re
from dataclasses import dataclass

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
    # moves: list

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

# yield the choices of next states
def choices(blueprint, state):
    # If we can build a geode robot, then do that
    if state.resources.can_spend(blueprint.geode_robot):
        yield State(state.resources - blueprint.geode_robot, state.robots + ResourceSpec(geode = 1)) #, state.moves + 'G')
        return
    if state.resources.can_spend(blueprint.obsidian_robot):
        yield State(state.resources - blueprint.obsidian_robot, state.robots + ResourceSpec(obsidian = 1)) #, state.moves + 'B')
        return
    # can always choose to do nothing
    yield State(state.resources, state.robots) #, state.moves + 'N')
    if state.resources.can_spend(blueprint.ore_robot):
        yield State(state.resources - blueprint.ore_robot, state.robots + ResourceSpec(ore = 1))# , state.moves + 'O')
    if state.resources.can_spend(blueprint.clay_robot):
        yield State(state.resources - blueprint.clay_robot, state.robots + ResourceSpec(clay = 1)) #, state.moves + 'C')

def simulate(blueprint, state, minutes):
    if minutes == 0:
        yield state
    else:
        for c in choices(blueprint, state):
            c.resources += c.robots
            yield from simulate(blueprint, c, minutes - 1)

def solve(blueprint, initial_state, minutes):
    return max(simulate(blueprint, initial_state, minutes), key=lambda state: state.resources.geode)

blueprints = map(parse_blueprint, sys.stdin)

minutes = 19

for blueprint in blueprints:
    initial_state = State(
        resources = ResourceSpec(),
        robots = ResourceSpec(ore = 1),
        #moves = ""
    )
    
    score = solve(blueprint, initial_state, minutes)
    print(f"{blueprint.id}, {score}")
    
