#!/usr/bin/env python3

from math import sqrt, floor, ceil
import sys

def win_comb(time, record):
    # This probably doesn't work if the roots are exact
    s1 = (time + sqrt(time * time - 4 * record)) / 2
    s2 = (time - sqrt(time * time - 4 * record)) / 2
    return floor(s1) - ceil(s2) + 1

times = next(sys.stdin).split(":")[1].split()
distances = next(sys.stdin).split(":")[1].split()
time = int("".join(times))
distance = int("".join(distances))
    
print(win_comb(time, distance))
