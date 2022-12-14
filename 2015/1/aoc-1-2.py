#!/usr/bin/env /usr/bin/python3

import sys
import itertools
from itertools import accumulate

char_scores = {
    '(': 1,
    ')': -1
}

line = sys.stdin.readline().rstrip()

scores = (char_scores[c] for c in line)
partial_scores = enumerate(accumulate(scores))
nps = (i for i, x in partial_scores if x < 0)
print(next(nps) + 1)


