#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass, field
from itertools import count


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

    def __str__(self):
        return self.name

@dataclass
class FlipFlop(Module):
    on: bool = False
    def process(self, pulse: Pulse):
        if not pulse.high:
            self.on = not self.on
            yield from (Pulse(self.name, self.on, d) for d in self.dests)

    def __str__(self):
        return f"f_{self.name}"

@dataclass
class Conjunction(Module):
    def process(self, pulse: Pulse):
        self.inputs[pulse.src] = pulse.high
        out = not all(self.inputs.values())
        yield from (Pulse(self.name, out, d) for d in self.dests)

    def __str__(self):
        return f"c_{self.name}"

@dataclass
class Untyped(Module):
    def process(self, pulse: Pulse):
        return
        yield # make it a generator

    def __str__(self):
        return self.name

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

lines = map(str.rstrip, sys.stdin)
modules = {m.name: m for m in map(parse, lines) }

# fill out inputs
for m in modules.values():
    for d in m.dests:
        if d in modules:
            modules[d].inputs[m.name] = False

# Add the extra module from the question
rxin = {m.name: False for m in modules.values() if "rx" in m.dests}
modules["rx"] = Untyped("rx", [], rxin)

print("digraph {")
for m in modules.values():
    for d in m.dests:
        d = modules[d]
        print(f"\t{m} -> {d}")

print("}")
