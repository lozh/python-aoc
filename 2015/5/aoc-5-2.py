#!/usr/bin/env /usr/bin/python3

import sys
import itertools

def iter_len(i):
    return sum(1 for _ in i)

# This is in itertools in Python 3.10
def pairwise(i):
    a, b = tee(i)
    next(b, None)
    return zip(a, b)

def repeated_pair(s):
    for i in range(len(s) - 1):
        p = s[i:i+2]
        if s.find(p, i+2) != -1:
            return True
    return False

def rule2(s):
    for i in range(len(s) - 2):
        if s[i] == s[i+2]:
            return True
    return False

def nice(s):
    return repeated_pair(s) and rule2(s)

print(iter_len(s for s in map(str.rstrip, sys.stdin) if nice(s)))

