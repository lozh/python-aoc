#!/usr/bin/env /usr/bin/python3

# Warning, this uses eval on stdin
import sys
import itertools
from itertools import zip_longest
import functools
from functools import cmp_to_key, reduce
import operator
from operator import mul

dividers = [[[2]], [[6]]]

def parse_packets(lines):
    # divider packets
    yield from dividers
    try:
        while True:
            # I manually checked the input
            yield eval(next(lines))
            yield eval(next(lines))
            # skip blank line
            _ = next(lines)
    except:
        pass

# 0 for exactly the same
# 1 for right order
# -1 for wrong order
def cmp_packets(p1, p2):
    # If I had a more recent python this might work as a match statement
    if p1 == None:
        return 1
    if p2 == None:
        return -1
    if p1 == p2:
        return 0
    if type(p1) is int and type(p2) is int:
        return 1 if p1 < p2 else -1
    if type(p1) is int:
        p1 = [p1]
    if type(p2) is int:
        p2 = [p2]
    for x, y in zip_longest(p1, p2):
        c = cmp_packets(x, y)
        if c != 0:
            return c
    return 0

def packets_in_order(p1, p2):
    return cmp_packets(p1, p2) >= 0
    
packets = parse_packets(sys.stdin)
packets = sorted(packets, key = cmp_to_key(cmp_packets), reverse = True)
print(reduce(mul, (packets.index(x) + 1 for x in dividers)))


