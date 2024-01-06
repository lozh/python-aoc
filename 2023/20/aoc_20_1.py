#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass, field


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
        pass

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

high = 0
low = 0
for i in range(1000):
    for p in simulate(modules):
        high += 1 if p.high else 0
        low += 0 if p.high else 1

print(high * low)
