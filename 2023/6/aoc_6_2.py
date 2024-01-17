#!/usr/bin/env python3

from math import sqrt, floor, ceil
import sys

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

times = next(sys.stdin).split(":")[1].split()
distances = next(sys.stdin).split(":")[1].split()
time = int("".join(times))
distance = int("".join(distances))
    
print(win_comb(time, distance))
