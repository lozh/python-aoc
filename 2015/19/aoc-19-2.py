#!/usr/bin/env /usr/bin/python3

import sys
import re
from itertools import count

line_re = re.compile("^(\w+) => (\w+)$")

def parse_input(lines):
    subs = []
    for line in lines:
        if not line:
            break

        m = line_re.match(line)
        f = m.group(1)
        subs.append((m.group(2), m.group(1)))
    molecule = next(lines)
    return molecule, subs

def fabricate(start, target, subs, steps):
    if start == target:
        yield steps
    else:
        for f, t in subs:
            i = start.find(f)
            while i >= 0:
                yield from fabricate(start[:i] + t + start[i + len(f):], target, subs, steps + 1)
                i = start.find(f, i + 1)

molecule, subs = parse_input(map(str.rstrip, sys.stdin))
subs = sorted(subs, key = lambda x: len(x[0]) - len(x[1]), reverse = True)
print(next(fabricate(molecule, "e", subs, 0)))
