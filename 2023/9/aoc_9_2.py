#!/usr/bin/env python3
from itertools import pairwise
import sys

def differences(l):
    yield from (y - x for x, y in pairwise(l))

def extrapolate(l):
    if all(x == 0 for x in l):
        return 0

    d = list(differences(l))

    return l[0] - extrapolate(d)

def parse(line):
    return list(map(int, line.split()))

lines = map(str.rstrip, sys.stdin)
seqs = map(parse, lines)

print(sum(map(extrapolate, seqs)))
