#!/usr/bin/env /usr/bin/python3

import sys

offsets = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0)
}

turns = {
    ('N', 'R'): 'E',
    ('N', 'L'): 'W',
    ('E', 'R'): 'S',
    ('E', 'L'): 'N',
    ('S', 'R'): 'W',
    ('S', 'L'): 'E',
    ('W', 'R'): 'N',
    ('W', 'L'): 'S',
}

def solve(instructions):
    pos = (0, 0)
    facing = 'N'
    visited = {pos}
    for i in instructions:
        t = i[0]
        d = int(i[1:])
        facing = turns[(facing, t)]
        offset = offsets[facing]
        for _ in range(d):
            pos = pos[0] + offset[0], pos[1] + offset[1]
            if pos in visited:
                return pos
            visited.add(pos)

            
dirs = sys.stdin.readline()
pos = solve(dirs.split(', '))
print(abs(pos[0]) + abs(pos[1]))            
