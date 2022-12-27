#!/usr/bin/env /usr/bin/python3

# Warning, this uses eval on stdin
import sys
from itertools import zip_longest

def parse_packets(lines):
    try:
        while True:
            # I manually checked the input
            p1 = eval(next(lines))
            p2 = eval(next(lines))
            yield (p1, p2)
            # skip blank line
            _ = next(lines)
    except:
        pass

# 0 for exactly the same
# 1 for right order
# -1 for wrong order
def cmp_packets(p1, p2):
    # print(f"p1 = {p1}, p2 = {p2}")
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

packets = (x + 1 for x, (p1, p2) in enumerate(parse_packets(sys.stdin)) if packets_in_order(p1, p2))
print(sum(packets))
