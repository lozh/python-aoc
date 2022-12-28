#!/usr/bin/env /usr/bin/python3

import sys

def solve(containers, target):
    for i in range(len(containers)):
        c = containers[i]
        if c == target:
            yield [c]
        elif c < target:
            for x in solve(containers[i+1:], target - c):
                yield [c] + x

containers = list(map(int, map(str.rstrip, sys.stdin)))

target = 150

sols = solve(containers, target)

lens = sorted(map(len, sols))

print(sum(1 for x in lens if x == lens[0]))


