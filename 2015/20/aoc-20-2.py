#!/usr/bin/env /usr/bin/python3

import sys
from dataclasses import dataclass
from itertools import count

@dataclass
class Elf:
    no: int
    next_house: int
    count: int

nexts = {}

target = int(sys.stdin.readline())

for i in count(1):
    e = Elf(no = i, next_house = i, count = 0)
    if not i in nexts:
        nexts[i] = []
    nexts[i].append(e)

    t = 0
    for e in nexts[i]:
        t += 11 * e.no
        e.next_house += e.no
        e.count += 1
        if e.count <= 50:
            if not e.next_house in nexts:
                nexts[e.next_house] = []
            nexts[e.next_house].append(e)
    if t >= target:
        print(i)
        break
    del nexts[i]
