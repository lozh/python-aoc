#!/usr/bin/env /usr/bin/python3

import sys
import re

parse_re = re.compile("^(\d+)-(\d+)$")

def parse_line(line):
    if m := parse_re.match(line):
        return int(m.group(1)), int(m.group(2))
    else:
        raise Exception(f"Could not parse line: {line}")

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
                cur = None
    if cur != None:
        yield cur

ranges = map(parse_line, sys.stdin)
ranges = consolidate_ranges(ranges)
range = next(ranges)
print(range[1] + 1)
