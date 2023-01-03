#!/usr/bin/env /usr/bin/python3

import sys
from collections import deque

elf_count = int(sys.stdin.readline().strip())

def solve(elf_count):
    elves = deque(range(elf_count))
    l = elf_count
    elves.rotate(-(l // 2))
    while l > 1:
        _ = elves.popleft()
        if l % 2 == 1:
            elves.rotate(-1)
        l -= 1

    return elves.pop() + 1

print(solve(elf_count))
