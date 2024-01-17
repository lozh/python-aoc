#!/usr/bin/env python3

import re
import sys
from dataclasses import dataclass
from functools import reduce
from operator import mul

def prod(iter):
    return reduce(mul, iter, 1)

@dataclass
class Race:
    time: int
    record: int

    def distance(self, press):
        return (self.time - press) * press

    def win_comb(self):
        return sum(1 for i in range(self.time) if self.distance(i) > self.record)

times = next(sys.stdin).split(":")[1].split()
distances = next(sys.stdin).split(":")[1].split()
races = [Race(int(t), int(d)) for (t, d) in zip(times, distances)]

print(prod(map(lambda x: x.win_comb(), races)))
