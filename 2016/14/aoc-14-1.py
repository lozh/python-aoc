#!/usr/bin/env /usr/bin/python3

import sys
from hashlib import md5
from collections import deque
from itertools import islice, count, repeat

def first_triple(s):
    for t in (s[i:i+3] for i in range(len(s) - 2)):
        if t[0] == t[1] and t[1]  == t[2]:
            return t[0]

def hashes(salt):
    for i in count():
        yield i, md5(f"{salt}{i}".encode()).digest().hex()

def keys(salt, size):
    h = hashes(salt)
    dq = deque(islice(h, size))
    while True:
        i, trial = dq.popleft()
        dq.append(next(h))
        if t := first_triple(trial):
            five = "".join(repeat(t, 5))
            if any(hs.find(five) != -1 for _, hs in dq):
                yield i, trial

size = 1000
key_count = 64
salt = sys.stdin.readline().strip()
k = keys(salt, size)
keys = list(islice(k, key_count))
print(keys.pop()[0])
