#!/usr/bin/env /usr/bin/python3

import sys
import re

instruction_re = re.compile("^(turn on|toggle|turn off) (\d+),(\d+) through (\d+),(\d+)$")

ops = {
    "turn on": lambda x: True,
    "toggle": lambda x: not x,
    "turn off": lambda x: False
}

def parse_instruction(line):
    m = instruction_re.match(line)
    return {
        "op": ops[m.group(1)],
        "box": (
            (int(m.group(2)), int(m.group(3))),
            (int(m.group(4)), int(m.group(5)))
        ),
    }

def init_lights():
    for _ in range(1000):
        yield [False for _ in range(1000)]

def block(start, end):
    x1, y1 = start
    x2, y2 = end
    yield from ((x, y) for x in range(x1, x2 + 1) for y in range (y1, y2 + 1))

def apply_instruction(lights, instruction):
    start, end = instruction["box"]
    op = instruction["op"]
    for (x, y) in block(start, end):
        lights[x][y] = op(lights[x][y])
    return lights

def apply_instructions(lights, instructions):
    for instruction in instructions:
        lights = apply_instruction(lights, instruction)
    return lights

lights = list(init_lights())

instructions = map(parse_instruction, sys.stdin)

lights = apply_instructions(lights, instructions)

print(sum(1 for x in lights for y in x if y))


