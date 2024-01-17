#!/usr/bin/env python3

import sys
from math import sqrt, floor, ceil
from functools import reduce
from operator import mul

def prod(iter):
    return reduce(mul, iter, 1)

# Distance follows a quadratic, so we can solve for the intercepts
# Need to be slightly careful if the roots are exact
# As these would only equal the time, not beat it
def win_comb(time, record):
    s1 = (time + sqrt(time * time - 4 * record)) / 2
    s2 = (time - sqrt(time * time - 4 * record)) / 2
    root = int(sqrt(time * time - 4 * record))
    r = floor(s1) - ceil(s2) + 1
    if root * root == time * time - 4 * record:
        r -= 2
    return r

times = map(int, next(sys.stdin).split(":")[1].split())
distances = map(int, next(sys.stdin).split(":")[1].split())

print(prod(map(lambda z: win_comb(*z), zip(times, distances))))
