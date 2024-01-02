#!/usr/bin/env python3

from dataclasses import dataclass
from math import sqrt, floor, ceil

def prod(iter):
    return reduce(mul, iter, 1)

@dataclass
class Race:
    time: int
    record: int

    def distance(self, press):
        return (self.time - press) * press

    def win_comb(self):
        # This probably doesn't work if the roots are exact
        s1 = (self.time + sqrt(self.time * self.time - 4 * self.record)) / 2
        s2 = (self.time - sqrt(self.time * self.time - 4 * self.record)) / 2
        return floor(s1) - ceil(s2) + 1
    
test = Race(71530, 940200)
actual = Race(61709066, 643118413621041)

print(actual.win_comb())
