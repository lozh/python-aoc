#!/usr/bin/env python3

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

    
test = [Race(7, 9), Race(15, 40), Race(30, 200)]
actual = [Race(61, 643), Race(70, 1184), Race(90, 1362), Race(66, 1041)]

print(prod(map(lambda x: x.win_comb(), actual)))
