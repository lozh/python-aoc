#!/usr/bin/env /usr/bin/python3

import sys

def parse_line(line):
    return [int(line[1:5].strip()), int(line[6:10].strip()), int(line[11:15].strip())]

def possible(sides):
    sides.sort()
    return sides[2] < sides[0] + sides[1]

def possibles():
    for line in map(str.rstrip, sys.stdin):
        sides = parse_line(line)
        yield possible(sides)

print(sum(1 for x in possibles() if x))
