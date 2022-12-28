#!/usr/bin/env /usr/bin/python3

import sys

def solve(containers, target):
    for i in range(len(containers)):
        c = containers[i]
        if c == target:
            yield c
        elif c < target:
            yield from solve(containers[i+1:], target - c)

containers = list(map(int, map(str.rstrip, sys.stdin)))

target = 150

print(sum(1 for _ in solve(containers, target)))

