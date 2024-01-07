#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass, field
from itertools import count
from math import lcm


@dataclass
class Module:
    name: str
    dests: list[str]
    inputs: dict[str, bool] = field(default_factory=dict)

@dataclass
class Pulse:
    src: str
    high: bool
    dest: str

    def __str__(self):
        h = "high" if self.high else "low"
        return f"{self.src} -{h}-> {self.dest}"

@dataclass
class Broadcaster(Module):
    def process(self, pulse: Pulse):
        yield from (Pulse(self.name, pulse.high, d) for d in self.dests)

@dataclass
class FlipFlop(Module):
    on: bool = False
    def process(self, pulse: Pulse):
        if not pulse.high:
            self.on = not self.on
            yield from (Pulse(self.name, self.on, d) for d in self.dests)

@dataclass
class Conjunction(Module):
    def process(self, pulse: Pulse):
        self.inputs[pulse.src] = pulse.high
        out = not all(self.inputs.values())
        yield from (Pulse(self.name, out, d) for d in self.dests)

@dataclass
class Untyped(Module):
    def process(self, pulse: Pulse):
        return
        yield # make it a generator

# line -> (name, type, list[dest])
def parse(line):
    m = re.match(r"([%&])?(\w+) -> (.*)", line)
    name = m[2]
    dests = m[3].split(", ")
    if name == "broadcaster":
        return Broadcaster(name, dests)
    if not m[1]:
        return Untyped(name, dests)
    if m[1] == '%':
        return FlipFlop(name, dests)
    if m[1] == '&':
        return Conjunction(name, dests)
    raise ValueError(f"Couldn't parse {line}")

def simulate(modules):
    pulses = [Pulse("button", False, "broadcaster")]
    while pulses:
        new_pulses = []
        for p in pulses:
            yield p
            if p.dest in modules:
                m = modules[p.dest]
                new_pulses.extend(m.process(p))
        pulses = new_pulses

lines = map(str.rstrip, sys.stdin)
modules = {m.name: m for m in map(parse, lines) }

# fill out inputs
for m in modules.values():
    for d in m.dests:
        if d in modules:
            modules[d].inputs[m.name] = False

# This is from looking at the specific graph
# and noting that there are 4 distinct subgraphs
# that join to a single conjuncion zh before the rx output
# detect cycles in each of the subgraphs
def detect_cycles(modules, dest):
    input_count = sum(1 for m in modules.values() if dest in m.dests)
    cycles = {}
    detected = set()
    for i in count(1):
        for p in simulate(modules):
            if p.dest == dest and p.high:
                if p.src in cycles and p.src not in detected:
                    yield(p.src, cycles[p.src], i - cycles[p.src])
                    detected.add(p.src)
                    if len(detected) == input_count:
                        return
                cycles[p.src] = i

# Add the extra module from the question
rxin = [m.name for m in modules.values() if "rx" in m.dests]
modules["rx"] = Untyped("rx", [], {n: False for n in rxin})

# from inspection, there is only one node with rx as an output
# from second inspection, each cycle is from the start, no offsets
cycles = [cycle for (src, count, cycle) in detect_cycles(modules, rxin[0])]
print(lcm(*cycles))



