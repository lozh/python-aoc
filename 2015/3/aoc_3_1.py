#!/usr/bin/env /usr/bin/python3

from itertools import accumulate
from typing import Iterable, Generator

# I'm on python 3.8.10, can't do useful type hints for *var
# want to say arbitary number of tuples of summable things
def tuple_add(*t: tuple) -> tuple:
    return tuple(map(sum, zip(*t)))

def travel(path: Iterable[tuple], start: tuple) -> Generator[tuple, None, None]:
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

