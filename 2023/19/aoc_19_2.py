#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from copy import deepcopy

@dataclass(frozen=True)
class Condition:
    arg1: str
    op: str
    arg2: int

    def negate(self):
        if self.op == '<':
            return Condition(self.arg1, '>', self.arg2 - 1)
        else:
            return Condition(self.arg1, '<', self.arg2 + 1)

class ConditionSet:
    conditions: dict[str, list[Condition]]

    def __init__(self):
        self.conditions = {}

    def add(self, condition: Condition):
        if condition.arg1 in self.conditions:
            cs = self.conditions[condition.arg1]
            for i, c in enumerate(cs):
                if c.op == condition.op:
                    if c.op == '>':
                        cs[i] = Condition(c.arg1, c.op, max(condition.arg2, c.arg2))
                        return
                    else:
                        cs[i] = Condition(c.arg1, c.op, min(condition.arg2, c.arg2))
                        return
            cs.append(condition)
        else:
            self.conditions[condition.arg1] = [condition]

    def __str__(self):
        s = ""
        for c in self.conditions:
            s += f"{c}, {self.conditions[c]}\n"
        return s

    def score(self, mi, mx):
        tot = 1
        for var in "xmas":
            l = mi
            h = mx
            for c in self.conditions.get(var, []):
                if c.op == '>':
                    l = c.arg2
                else:
                    h = c.arg2
            tot *= (h - l - 1)
        return tot

@dataclass(frozen=True)
class Rule:
    condition: Condition
    dest: str

@dataclass(frozen=True)
class Workflow:
    name: str
    rules: list[Rule]

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

def parse(lines) -> (dict[str, Workflow]):
    workflows = {}

    while (line := next(lines)) != "":
        w = parse_workflow(line)
        workflows[w.name] = w

    return workflows

def find_condition_sets(workflows, current, conditions):
    negative_conditions = []
    for r in current.rules:
        cs = deepcopy(conditions)
        for nn in negative_conditions:
            cs.add(nn)
            
        if r.condition:
            cs.add(r.condition)
            negative_conditions.append(r.condition.negate())

        if r.dest == 'R' or r.dest == 'A':
            yield (r.dest, cs)
        else:
            yield from find_condition_sets(workflows, workflows[r.dest], cs)

lines = map(str.rstrip, sys.stdin)
workflows = parse(lines)
cs = find_condition_sets(workflows, workflows["in"], ConditionSet())

print(sum(c.score(0, 4001) for d, c in cs if d == 'A'))


