#!/usr/bin/env python3

import sys
from functools import reduce

def line_to_pair(line):
    x = line.split()
    return (int(x[0]), int(x[1]))

stdin = map(str.rstrip, sys.stdin)
pairs = map(line_to_pair, stdin)

lid_lists = [list(t) for t in zip(*pairs)]

l1 = sorted(lid_lists[0])
l2 = sorted(lid_lists[1])

print(sum(map(lambda a, b: abs(a - b), l1, l2)))

