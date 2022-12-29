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

pos = (0, 0)
facing = 'N'

dirs = sys.stdin.readline()

for i in dirs.split(', '):
    t = i[0]
    d = int(i[1:])
    facing = turns[(facing, t)]
    offset = offsets[facing]
    pos = pos[0] + offset[0] * d, pos[1] + offset[1] * d

print(abs(pos[0]) + abs(pos[1]))
