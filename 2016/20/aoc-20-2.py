#!/usr/bin/env /usr/bin/python3

import sys
import re
from itertools import tee

parse_re = re.compile("^(\d+)-(\d+)$")

def parse_line(line):
    if m := parse_re.match(line):
        return int(m.group(1)), int(m.group(2))
    else:
        raise Exception(f"Could not parse line: {line}")

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def consolidate_ranges(ranges):
    ranges = sorted(ranges)
    cur = None
    for r in ranges:
        if cur == None:
            cur = r
        else:
            if r[0] <= cur[1] + 1:
                # ranges overlap
                cur = cur[0], max(cur[1], r[1])
            else:
                yield cur
                cur = r
    if cur != None:
        yield cur

def gaps(ranges):
    for r1, r2 in pairwise(ranges):
        yield r2[0] - r1[1] - 1

ranges = map(parse_line, sys.stdin)
ranges = consolidate_ranges(ranges)
ranges = list(ranges)
ranges.append((4294967296, 4294967296))
print(sum(gaps(ranges)))
