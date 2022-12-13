#!/usr/bin/env /usr/bin/python3

import sys
import re
from collections import deque

# returns iterable of (stack#, letter)
def parse_stack(line):
    pos = 0
    while pos * 4 < len(line):
        x = line[pos * 4 + 1]
        if x != ' ':
            yield (pos, x)
        pos = pos + 1

def is_stack(line):
    return line.__contains__("[")

instruction_re = re.compile("^move (\d+) from (\d+) to (\d+)$")

# returns (count, source, dest)
def parse_instruction(line):
    m = instruction_re.match(line)
    return int(m.group(1)), int(m.group(2)) - 1, int(m.group(3)) - 1

def parse_input(lines):
    stacks = []
    instructions = []
    in_stack = True
    in_blank = False
    for line in lines:
        if in_stack:
            if is_stack(line):
                for id, letter in parse_stack(line):
                    while len(stacks) <= id:
                        stacks.append([])
                    stacks[id].append(letter)
            else:
                # deal with blank stacks on the right only indicated by the numbers
                for id, letter in parse_stack(line):
                    while len(stacks) <= id:
                        stacks.append([])
                in_stack = False
                in_blank = True
        elif in_blank:
            #skip
            in_blank = False
            for stack in stacks:
                # want to be able to push and pop to indicate moving
                stack.reverse()
        else:
            instructions.append(parse_instruction(line))
    return stacks, instructions

def apply_instruction(stacks, instruction):
    count, source, dest = instruction
    pile = list(stacks[source][-count:])
    stacks[source] = stacks[source][0:-count]
    stacks[dest] = stacks[dest] + pile
    return stacks

stdin = map(str.rstrip, sys.stdin)

stacks, instructions = parse_input(stdin)

for instruction in instructions:
    stacks = apply_instruction(stacks, instruction)

tops = map(lambda x: x.pop(), stacks)
print(''.join(tops))
