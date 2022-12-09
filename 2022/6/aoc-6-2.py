#!/usr/bin/env /usr/bin/python3

import sys

stdin = sys.stdin.read().splitlines()
line = stdin[0]

size = 14
i = size

while i < len(line):
    s = line[i - size: i]
    if (len(set(s)) == size):
        print(i)
        break
    i = i + 1

