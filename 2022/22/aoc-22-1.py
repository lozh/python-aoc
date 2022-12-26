#!/usr/bin/env /usr/bin/python3

import sys
import re

dir_rotates = {
    ('>', 'R'): 'v',
    ('>', 'L'): '^',
    ('<', 'R'): '^',
    ('<', 'L'): 'v',
    ('^', 'R'): '>',
    ('^', 'L'): '<',
    ('v', 'R'): '<',
    ('v', 'L'): '>',
}

dir_offsets = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1),
}

dir_scores = {
    '>': 0,
    'v': 1,
    '<': 2,
    '^': 3,
}

move_re = re.compile("^(\d+)(.*)")
rotate_re = re.compile("(L|R)(.*)")
def parse_input(lines):
    layout = []
    instructions = []
    for line in map(str.rstrip, lines):
        if line == "":
            break
        layout.append(line)

    instr = next(lines)
    while True:
        m = move_re.match(instr)
        if m:
            instructions.append(int(m.group(1)))
            instr = m.group(2)
        else:
            break
        m = rotate_re.match(instr)
        if m:
            instructions.append(m.group(1))
            instr = m.group(2)
        else:
            break

    return layout, instructions

def get_bounds(layout):
    return (max(map(len, layout)), len(layout))

def find_start(layout):
    i = layout[0].index(".")
    return (i, 0)

def add_pos(pos, offset, bounds):
    x, y  = pos[0] + offset[0], pos[1] + offset[1]
    if offset[1] > 0 and y >= bounds[1]:
        y = 0
    if offset[1] < 0 and y < 0:
        y = bounds[1] - 1
    if offset[0] > 0 and x >= bounds[0]:
        x = 0
    if offset[0] < 0 and x < 0:
        x = bounds[0] - 1
    return x, y

def next_in_dir(layout, pos, offset, bounds):
    while True:
        x, y = add_pos(pos, offset, bounds)
        if x < len(layout[y]):
            if layout[y][x] == ".":
                return x, y
            if layout[y][x] == "#":
                return None
        pos = x, y
        
def move(layout, pos, dir, count, bounds):
    offset = dir_offsets[dir]
    for _ in range(count):
        n = next_in_dir(layout, pos, offset, bounds)
        if n == None:
            return pos
        pos = n
    return n
    
def simulate(layout, instructions):
    bounds = get_bounds(layout)
    pos = find_start(layout)
    dir = '>'

    is_move = True
    
    for i in instructions:
        if is_move:
            pos = move(layout, pos, dir, i, bounds)
            is_move = False
        else:
            dir = dir_rotates[(dir, i)]
            is_move = True

    return pos, dir

layout, instructions = parse_input(sys.stdin)
(col, row), dir = simulate(layout, instructions)

print(1000 * (row + 1) +  4 * (col + 1) + dir_scores[dir])
