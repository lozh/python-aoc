#!/usr/bin/env python3

import sys

def line_to_pair(line):
    x = line.split()
    return (int(x[0]), int(x[1]))

stdin = map(str.rstrip, sys.stdin)
pairs = map(line_to_pair, stdin)

lid_lists = [list(t) for t in zip(*pairs)]

l1 = lid_lists[0]
l2 = lid_lists[1]

sims = map(lambda x: x * l2.count(x), l1)
print(sum(sims))
