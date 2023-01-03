#!/usr/bin/env /usr/bin/python3

import sys


elves = list(range(int(sys.stdin.readline().strip())))
i = 1

while len(elves) > 1:
    if i  >= len(elves):
        i = i - len(elves)
        elves = [x for x in elves if x != None]
    else:
        elves[i] = None
        i += 2

print(elves[0]+1)
