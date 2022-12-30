#!/usr/bin/env /usr/bin/python3

import sys
import re
from dataclasses import dataclass

@dataclass
class Bot:
    lo: int
    hi: int
    carry: list


value_re = re.compile("^value (\d+) goes to bot (\d+)$")
rule_re = re.compile("^bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)$")

def build_world(lines):
    bots = {}
    rules = {}
    outputs = {}
    for line in lines:
        if m:= value_re.match(line):
            b = int(m.group(2))
            v = int(m.group(1))
            if not b in bots:
                bots[b] = []
            bots[b].append(v)
        elif m:= rule_re.match(line):
            b = int(m.group(1))
            lt = m.group(2)
            l = int(m.group(3))
            ht = m.group(4)
            h = int(m.group(5))
            if not b in bots:
                bots[b] = []
            rules[b] = ((lt, l), (ht, h))
        else:
            raise Exception(f"Could not parse input line {line}")
    return bots, rules, outputs

def iterate(bots, rules, outputs, seek):
    while True:
        for i, b in bots.items():
            if len(b) == 2:
                bl = min(b)
                bh = max(b)
                if (bl, bh) == seek:
                    return i
                (lt, l), (ht, h) = rules[i]
                if lt == "bot":
                    bots[l].append(bl)
                else:
                    outputs[l] = bl
                if ht == "bot":
                    bots[h].append(bh)
                else:
                    outputs[l] = bh
                del b[1]
                del b[0]


bots, rules, outputs = build_world(sys.stdin)
seek = (17, 61)

print(iterate(bots, rules, outputs, seek))
