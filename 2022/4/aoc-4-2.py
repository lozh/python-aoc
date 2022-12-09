#!/usr/bin/env /usr/bin/python3

import sys
import re

line_re = re.compile("^(\d+)-(\d+),(\d+)-(\d+)$")

def parse_input(line):
    m = line_re.match(line)
    return range(int(m.group(1)), int(m.group(2)) + 1), range(int(m.group(3)), int(m.group(4)) + 1)

def range_subset_of(r1, r2):
    return min(r1) >= min(r2) and max(r1) <= max(r2)

def disjoint(r1, r2):
    return max(r1) < min(r2) or max(r2) < min(r1)

def total_overlap(r1, r2):
    return range_subset_of (r1, r2) or range_subset_of(r2, r1)

stdin = sys.stdin.read().splitlines()
ranges = map(parse_input, stdin)

print(len(list(filter(lambda t: not disjoint(t[0], t[1]), ranges))))
