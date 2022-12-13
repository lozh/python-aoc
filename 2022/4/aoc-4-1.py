#!/usr/bin/env /usr/bin/python3

import sys
import re

line_re = re.compile("^(\d+)-(\d+),(\d+)-(\d+)$")

def parse_input(line):
    m = line_re.match(line)
    return range(int(m.group(1)), int(m.group(2)) + 1), range(int(m.group(3)), int(m.group(4)) + 1)

def range_subset_of(r1, r2):
    return min(r1) >= min(r2) and max(r1) <= max(r2)

def total_overlap(r1, r2):
    return range_subset_of (r1, r2) or range_subset_of(r2, r1)

stdin = map(str.rstrip, sys.stdin)
ranges = map(parse_input, stdin)

print(sum(1 for _ in filter(lambda t: total_overlap(t[0], t[1]), ranges)))
