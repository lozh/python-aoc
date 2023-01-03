#!/usr/bin/env /usr/bin/python3

import sys
from itertools import islice

traps = [
    [False, False, True],
    [False, True, True],
    [True, False, False],
    [True, True, False],
]

def next_line(line):
    l = [False] + line + [False]
    ret = []
    for x in range(len(l) - 2):
        ret.append(l[x:x+3] in traps)

    return ret

def lines(start):
    while True:
        yield start
        start = next_line(start)

start = sys.stdin.readline().strip()
start = list(x == '^' for x in start)
iter_count = 40

rows = islice(lines(start), iter_count)
safe_count = sum(1 for row in rows for x in row if not x)
print(safe_count)

