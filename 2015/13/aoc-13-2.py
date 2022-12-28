#!/usr/bin/env /usr/bin/python3

import sys
import re
from itertools import permutations, tee
from collections import Counter

line_re = re.compile("^(\w+) would (lose|gain) (\d+) happiness units? by sitting next to (\w+)\.$")

def parse_line(line):
    m = line_re.match(line)
    n1 = m.group(1)
    n2 = m.group(4)
    h = int(m.group(3))
    if m.group(2) == "lose":
        h = -h
    return n1, n2, h

# This is in itertools in Python 3.10
def pairwise(i):
    a, b = tee(i)
    next(b, None)
    return zip(a, b)

def score(arrangement, edges):
    s = edges[(arrangement[0], arrangement[len(arrangement) - 1])]
    for s1, s2 in pairwise(arrangement):
        s += edges[(s1, s2)]
    return s

def scores(people, edges):
    people = list(people)
    a = people.pop()
    for p in permutations(people):
        yield score(p + (a,), edges)

people = set()
edges = Counter()

for line in sys.stdin:
    n1, n2, h = parse_line(line)
    people.add(n1)
    people.add(n2)
    edges[(n1, n2)] += h
    edges[(n2, n1)] += h

for p in people:
    edges[("me", p)] = 0
    edges[(p, "me")] = 0

people.add("me")

print(max(scores(people, edges)))
