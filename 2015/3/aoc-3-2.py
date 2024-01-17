#!/usr/bin/env /usr/bin/python3

import sys
import itertools
from itertools import tee

offsets = {
    '^': (0, 1),
    'v': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
}

def tuple_add(*t):
    return tuple(map(sum, zip(*t)))

def simulate_path(start, path, f):
    for x in (x for i, x in enumerate(path) if f(i)):
        start = tuple_add(start, x)
        yield start

def simulate(start, path):
    yield start
    a, b = tee(path)
    yield from simulate_path(start, a, lambda i: i % 2 == 0)
    yield from simulate_path(start, b, lambda i: i % 2 == 1)

start = (0, 0)
instructions = sys.stdin.readline().rstrip()
path = (offsets[i] for i in instructions)
print(len(set(simulate(start, path))))

