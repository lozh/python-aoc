#!/usr/bin/env /usr/bin/python3

import sys
from itertools import islice

# takes three lists of three numbers and yields three prospective triangles
def parse_triangles(l):
    yield [l[0][0], l[1][0], l[2][0]]
    yield [l[0][1], l[1][1], l[2][1]]
    yield [l[0][2], l[1][2], l[2][2]]

def parse_line(line):
    return [int(line[1:5].strip()), int(line[6:10].strip()), int(line[11:15].strip())]

def chunks(iter, n):
    while chunk:= list(islice(iter, n)):
        yield chunk

def possible(sides):
    sides.sort()
    return sides[2] < sides[0] + sides[1]

def possibles():
    i = map(parse_line,  map(str.rstrip, sys.stdin))
    for l in chunks(i, 3):
        for t in parse_triangles(l):
            yield possible(t)

print(sum(1 for x in possibles() if x))
