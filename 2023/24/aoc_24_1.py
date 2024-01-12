#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from itertools import combinations
from typing import TypeVar

Self = TypeVar("Self", bound="Hailstone")

@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    def position_xy_at_t(self, t) -> (int, int):
        if t:
            return (self.x + t * self.vx, self.y + t * self.vy)
        else:
            return None

    # return (x, y) if intersect in both futures or None otherwise
    def intersect_t(self, other: Self) -> (int, int):
        d = self.vx * other.vy - other.vx * self.vy
        if not d:
            # Parallel
            return None

        t = other.vx * self.y + other.x * other.vy - other.vx * other.y - other.vy * self.x
        return t / d

    @classmethod
    def parse(cls, line) -> Self:
        m = re.match(r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)", line)
        return cls(int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5]), int(m[6]))

lines = map(str.rstrip, sys.stdin)
hailstones = map(Hailstone.parse, lines)

xmin = 200000000000000
ymin = 200000000000000
xmax = 400000000000000
ymax = 400000000000000

c = 0
for (h1, h2) in combinations(hailstones, 2):
    t1 = h1.intersect_t(h2)
    t2 = h2.intersect_t(h1)
    if t1:
        if t1 >= 0 and t2 >= 0:
            x, y = h1.position_xy_at_t(t1)
            if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                c += 1

print(c)
