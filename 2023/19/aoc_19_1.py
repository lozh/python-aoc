#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Part:
    vals: dict[str, int]

    def score(self):
        return sum(self.vals.values())

@dataclass(frozen=True)
class Condition:
    arg1: str
    op: str
    arg2: int

    def ok(self, part: Part) -> bool:
        v = part.vals[self.arg1]
        match self.op:
            case '>':
                return v > self.arg2
            case '<':
                return v < self.arg2
        raise ValueError("Broken Condition.ok({self}, part)")

@dataclass(frozen=True)
class Rule:
    condition: Condition
    dest: str

    def ok(self, part: Part) -> bool:
        if not self.condition:
            return True
        else:
            return self.condition.ok(part)

@dataclass(frozen=True)
class Workflow:
    name: str
    rules: list[Rule]

    def dest(self, part: Part) -> str:
        for r in self.rules:
            if r.ok(part):
                return r.dest
        raise ValueError("Broken Workflow.dest({self, part})")

def parse_condition(s: str) -> Condition:
    if not s:
        return None

    m = re.match(r"([xmas])([<>])(\d+)", s)
    return Condition(m[1], m[2], int(m[3]))

def parse_rule(s: str) -> Rule:
    m = re.match(r"(?:([^:]+):)?(\w+)", s)
    return Rule(parse_condition(m[1]), m[2])

def parse_workflow(line: str) -> Workflow:
    m = re.match(r"(\w+)\{([^}]+)\}", line)
    name = m[1]
    rules = list(map(parse_rule, m[2].split(",")))
    return Workflow(name, rules)

def parse_part(line: str):
    m = re.match(r"\{([^}]+)\}", line)
    vals = {}
    for a in m[1].split(","):
        e = re.match(r"([xmas])=(\d+)", a)
        vals[e[1]] = int(e[2])

    return Part(vals)

def parse(lines) -> (dict[str, Workflow], list[Part]):
    workflows = {}
    parts = []

    while (line := next(lines)) != "":
        w = parse_workflow(line)
        workflows[w.name] = w

    while line := next(lines, None):
        parts.append(parse_part(line))

    return (workflows, parts)

def destination(workflows, part):
    dest = "in"
    while dest != 'R' and dest != 'A':
        w = workflows[dest]
        dest = w.dest(part)
    return dest

lines = map(str.rstrip, sys.stdin)

workflows, parts = parse(lines)

print(sum(p.score() for p in parts if destination(workflows, p) == 'A'))
