#!/usr/bin/env /usr/bin/python3

import sys

def find_common(l):
    s1, s2, s3 = l
    x = list(set(s1) & set(s2) & set(s3))[0]
    return x

def sub_lists(l, size):
    while len(l) > 0:
        yield l[0:size]
        l = l[size:]

def score(c):
    if c >= 'a' and c <= 'z':
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27

stdin = sys.stdin.read().splitlines()
triples = sub_lists(stdin, 3)
common = map(find_common, triples)
scores = map(score, common)
print(sum(scores))
