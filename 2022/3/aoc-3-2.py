#!/usr/bin/env /usr/bin/python3

import sys

def find_common(l):
    s1, s2, s3 = l
    return next(iter(set(s1) & set(s2) & set(s3)))

def sub_lists(l, size):
    r = []
    for e in l:
        if len(r) == size:
            yield r
            r = []
        r.append(e)

def score(c):
    if c >= 'a' and c <= 'z':
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27

stdin = map(str.rstrip, sys.stdin)
triples = sub_lists(stdin, 3)
common = map(find_common, triples)
scores = map(score, common)
print(sum(scores))
