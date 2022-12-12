#!/usr/bin/env /usr/bin/python3

import sys
from itertools import takewhile

x = 1
cycle = 1

def pixel(cycle, x):
    col = (cycle - 1) % 40
    if col >= (x - 1) and col <= (x + 1):
        return "#"
    else:
        return "."

def execute_instruction(instr, args, cycle, x):
    if instr == "noop":
        yield cycle + 1, x
    if instr == "addx":
        yield cycle + 1, x
        yield cycle + 2, x + int(args[0])

def execute(stdin, cycle, x):
    yield cycle, x
    for line in stdin:
        instr, *args = line.split(' ')
        for cycle, x in execute_instruction(instr, args, cycle, x):
            yield cycle, x

stdin = sys.stdin.read().splitlines()

states = takewhile(lambda pos: pos[0] <= 240, execute(stdin, cycle, x))
pixels = map(lambda pos: pixel(pos[0], pos[1]), states)
flat_screen = ''.join(pixels)
scan_lines = [flat_screen[i:i+40] for i in range(0, len(flat_screen), 40)]
for scan_line in scan_lines:
    print(scan_line)
