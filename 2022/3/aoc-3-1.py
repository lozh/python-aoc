#!/usr/bin/env /usr/bin/python3

import sys

def find_common(pair):
    s1, s2 = pair
    # we're only expecting one overlap
    return next(iter(set(s1) & set(s2)))

def half_line(s):
    n = len(s) // 2
    return s[0:n], s[n:]

def score(c):
    if c >= 'a' and c <= 'z':
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27

stdin = map(str.rstrip, sys.stdin)
half_lines = map(half_line, stdin)
common = map(find_common, half_lines)
scores = map(score, common)
print(sum(scores))
