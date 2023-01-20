#!/usr/bin/env /usr/bin/python3

import sys
from itertools import accumulate, chain

offsets = {
    '^': (0, 1),
    'v': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
}

def tuple_add(*t):
    return tuple(map(sum, zip(*t)))

instructions = sys.stdin.readline().rstrip()
path = (offsets[i] for i in instructions)
print(len(set(accumulate(path, tuple_add))))

