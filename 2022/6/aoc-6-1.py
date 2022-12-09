#!/usr/bin/env /usr/bin/python3

import sys

stdin = sys.stdin.read().splitlines()
line = stdin[0]

i = 4

while i < len(line):
    s = line[i - 4: i]
    if (len(set(s)) == 4):
        print(i)
        break
    i = i + 1

