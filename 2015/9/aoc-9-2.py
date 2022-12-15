#!/usr/bin/env /usr/bin/python3

import sys
import re
import itertools
from itertools import permutations, tee

# This is in itertools in Python 3.10
def pairwise(i):
    a, b = tee(i)
    next(b, None)
    return zip(a, b)

dist_re = re.compile("^(\w+) to (\w+) = (\d+)$")

def parse_line(line):
    m = dist_re.match(line)
    return m.group(1), m.group(2), int(m.group(3))

def parse_input(lines):
    places = set()
    distances = {}

    for s, d, l in map(parse_line, lines):
        places.add(s)
        places.add(d)
        distances[(s, d)] = l
        distances[(d, s)] = l

    return places, distances

def distance(route, distances):
    return sum(distances[h] for h in pairwise(route))

def route_distances(places, distances):
    for route in permutations(places):
        yield distance(route, distances)

lines = map(str.rstrip, sys.stdin)
places, distances = parse_input(lines)
print(max(route_distances(places, distances)))
