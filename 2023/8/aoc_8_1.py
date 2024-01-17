#!/usr/bin/env python3

from dataclasses import dataclass
import itertools
import sys
import re

@dataclass
class Node:
    left: str
    right: str

def parse_line(line):
    m = re.match(r"(...) = \((...), (...)\)", line)
    return m[1], Node(m[2], m[3])

def parse(lines):
    return {key: value for key, value in map(parse_line, lines)}

lines = map(str.rstrip, sys.stdin)

moves = next(lines)
_ = next(lines)

net = parse(lines)

mc = 0
curr = "AAA"

for move in itertools.cycle(moves):
    if curr == "ZZZ":
        break
    mc += 1;
    if move == 'L':
        curr = net[curr].left
    else:
        curr = net[curr].right

print(mc)
