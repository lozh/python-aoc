#!/usr/bin/env python3

from dataclasses import dataclass
from math import sqrt, floor, ceil
import sys

@dataclass
class Race:
    time: int
    record: int

    def win_comb(self):
        # This probably doesn't work if the roots are exact
        s1 = (self.time + sqrt(self.time * self.time - 4 * self.record)) / 2
        s2 = (self.time - sqrt(self.time * self.time - 4 * self.record)) / 2
        return floor(s1) - ceil(s2) + 1

times = next(sys.stdin).split(":")[1].split()
distances = next(sys.stdin).split(":")[1].split()
race = Race(int("".join(times)), int("".join(distances)))
    
print(race.win_comb())
