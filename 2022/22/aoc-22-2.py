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

edges = {}

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

def add_pos(pos, dir, offset, bounds, edges):
    x, y = pos
    if (x, y, dir) in edges:
        return edges[(x, y, dir)]
    x, y  = pos[0] + offset[0], pos[1] + offset[1]
    if offset[1] > 0 and y >= bounds[1]:
        y = 0
    if offset[1] < 0 and y < 0:
        y = bounds[1] - 1
    if offset[0] > 0 and x >= bounds[0]:
        x = 0
    if offset[0] < 0 and x < 0:
        x = bounds[0] - 1
    return x, y, dir

def next_in_dir(layout, pos, dir, bounds, edges):
    while True:
        offset = dir_offsets[dir]
        x, y, dir = add_pos(pos, dir, offset, bounds, edges)
        if len(layout[y]) < x:
            print(f"{x},{y},{pos},{dir}")
        if layout[y][x] == ".":
            return x, y, dir
        if layout[y][x] == "#":
            return None
        pos = x, y
        
def move(layout, pos, dir, count, bounds, edges):
    for _ in range(count):
        n = next_in_dir(layout, pos, dir, bounds, edges)
        if n == None:
            x, y = pos
            return x, y, dir
        x, y, dir = n
        pos = x, y
    return n

def create_edges():
    # This is hard coded to our input
    edges = {}
    for x in range(0, 50):
        # face 1 to face 6
        edges[(50 + x, 0, '^')] = (0, 150 + x, '>')
        edges[(0, 150 + x, '<')] = (50 + x, 0, 'v')
        # face 2 to face 6
        edges[(100 + x, 0, '^')] = (x, 199, '^')
        edges[(x, 199, 'v')] = (100 + x, 0, 'v')
        # face 2 to face 4
        edges[(149, x, '>')] = (99, 149 - x, '<')
        edges[(99, 149 - x, '>')] = (149, x, '<')
        # face 2 to face 3
        edges[(100 + x, 49, 'v')] = (99, 50 + x, '<')
        edges[(99, 50 + x, '>')] = (100 + x, 49, '^')
        # face 3 to face 5
        edges[(50, 50 + x, '<')] = (x, 100, 'v')
        edges[(x, 100, '^')] = (50, 50 + x, '>')
        # face 4 to face 6
        edges[(50 + x, 149, 'v')] = (49, 150 + x, '<')
        edges[(49, 150 + x, '>')] = (50 + x, 149, '^')
        # face 1 to face 5
        edges[(50, x, '<')] = (0, 149 - x, '>')
        edges[(0, 149 - x, '<')] = (50, x, '>')
    return edges

def simulate(layout, instructions, edges):
    bounds = get_bounds(layout)
    pos = find_start(layout)
    dir = '>'

    is_move = True
    
    for i in instructions:
        if is_move:
            x, y, dir = move(layout, pos, dir, i, bounds, edges)
            pos = x, y
            is_move = False
        else:
            dir = dir_rotates[(dir, i)]
            is_move = True

    return pos, dir



layout, instructions = parse_input(sys.stdin)
edges = create_edges()
(col, row), dir = simulate(layout, instructions, edges)

print(1000 * (row + 1) +  4 * (col + 1) + dir_scores[dir])
