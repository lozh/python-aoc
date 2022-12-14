#!/usr/bin/env /usr/bin/python3

import sys

char_scores = {
    '(': 1,
    ')': -1
}

line = sys.stdin.readline().rstrip()

print(sum(char_scores[c] for c in line))
