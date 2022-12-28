#!/usr/bin/env /usr/bin/python3

import sys
import re

spec = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

sue_re = re.compile("^Sue (\d+): (.*)$")
stat_re = re.compile("(\w+): (\d+),? ?(.*)$")

def parse_sue(line):
    m = sue_re.match(line)
    sue = {
        "id": int(m.group(1))
    }
    stats = m.group(2)
    while stats:
        m = stat_re.match(stats)
        sue[m.group(1)] = int(m.group(2))
        stats = m.group(3)

    return sue

def check_sue(sue, spec):
    for k in sue:
        if k in spec:
            if sue[k] != spec[k]:
                return False
    return True

sues = map(parse_sue, sys.stdin)

sues = filter(lambda s: check_sue(s, spec), sues)

print(list(sues))

