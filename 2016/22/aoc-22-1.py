#!/usr/bin/env /usr/bin/python3

import sys
import re
from dataclasses import dataclass
from itertools import product

parse_re = re.compile("^/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%$")

@dataclass(frozen=True)
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int
    use_percent: int


def parse_line(line):
    if m := parse_re.match(line):
        return Node(
            x = int(m.group(1)),
            y = int(m.group(2)),
            size = int(m.group(3)),
            used = int(m.group(4)),
            avail = int(m.group(5)),
            use_percent = int(m.group(6))
        )
    else:
        raise Exception(f"Could not parse line {line}")

inp = sys.stdin
_ = next(inp)
_ = next(inp)
nodes = map(parse_line, inp)

print(sum(1 for a, b in product(nodes, repeat = 2) if a != b and a.used > 0 and a.used < b.avail))
