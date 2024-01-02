#!/usr/bin/env python3

from dataclasses import dataclass
import itertools
import sys
import re
from math import lcm

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
mlen = len(moves)
net = parse(lines)

# array of dictionaries, each with location -> cycle#
# where cycle is one complete run of moves
curr = (k for k in net if k[2] == 'A')


# After inspection, every start hits an end after using all the
# moves many times. This then repeats.
# So, we can solve the simpler problem of finding the lcm
# of the cycle sizes
# generators is a list of cycle sizes
generators = []

for c in curr:
    mc = 0
    for move in itertools.cycle(moves):
        if c[2] == 'Z':
            generators.append(mc)
            if (mc % mlen != 0):
                # check the assumption that we use all the moves
                # exactly before cycling
                print("Assumption Broken")
            break
        mc += 1
        c = net[c].left if move == 'L' else net[c].right

print(lcm(*generators))


