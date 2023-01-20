#!/usr/bin/env /usr/bin/python3

from itertools import accumulate


def tuple_add(*t):
    return tuple(map(sum, zip(*t)))

def travel(path, start):
    yield from accumulate(path, tuple_add, initial = start)

if __name__ == "__main__":
    import sys

    offsets = {
        '^': (0, 1),
        'v': (0, -1),
        '>': (1, 0),
        '<': (-1, 0),
    }

    instructions = sys.stdin.readline().rstrip()
    path = (offsets[i] for i in instructions)
    print(len(set(travel(path, (0,0)))))

