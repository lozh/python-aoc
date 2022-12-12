#!/usr/bin/env /usr/bin/python3

import sys
from itertools import takewhile

x = 1
cycle = 1

def execute_instruction(instr, args, cycle, x):
    if instr == "noop":
        yield cycle + 1, x
    if instr == "addx":
        yield cycle + 1, x
        yield cycle + 2, x + int(args[0])

def execute(stdin, cycle, x):
    for line in stdin:
        instr, *args = line.split(' ')
        for cycle, x in execute_instruction(instr, args, cycle, x):
            yield cycle, x

stdin = sys.stdin.read().splitlines()

states = takewhile(lambda pos: pos[0] <= 220, execute(stdin, cycle, x))
powers = filter(lambda pos : (pos[0] - 20) % 40 == 0, states)
powers = map(lambda x: x[0] * x[1], powers)

print(sum(powers))
