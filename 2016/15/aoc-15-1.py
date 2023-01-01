#!/usr/bin/env /usr/bin/python3

import sys
import re
from dataclasses import dataclass
from itertools import count

@dataclass(frozen=True)
class Disc:
    no: int
    npos: int
    start_pos: int
    # If we dropped coin at time t, is slot in pos 0 as it passes?
    def slot_at_t(self, t):
        return ((self.start_pos + t + self.no) % self.npos) == 0

parse_re = re.compile("^Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\.$")

def parse_line(line):
    if m := parse_re.match(line):
        return Disc(
            no = int(m.group(1)),
            npos = int(m.group(2)),
            start_pos = int(m.group(3))
        )
    raise Exception(f"Could not parse: {line}")

def solve(discs):
    for t in count():
        if all(d.slot_at_t(t) for d in discs):
            return t

discs = list(map(parse_line, sys.stdin))
print(solve(discs))

