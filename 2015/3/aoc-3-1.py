#!/usr/bin/env /usr/bin/python3

import sys

offsets = {
    '^': (0, 1),
    'v': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
}

def tuple_add(x, y):
    return tuple(a + b for (a, b) in zip(x, y))

def simulate(start, path):
    yield start
    for x in path:
        start = tuple_add(start, x)
        yield start

start = (0, 0)
instructions = sys.stdin.readline().rstrip()
path = (offsets[i] for i in instructions)
print(len(set(simulate(start, path))))

