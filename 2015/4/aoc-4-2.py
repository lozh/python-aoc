#!/usr/bin/env /usr/bin/python3

import sys
import itertools
from itertools import count
import hashlib
from hashlib import md5

def is_valid(coin, mask):
    return all(map(lambda x: x == 0, (a & b for a, b in zip(coin, mask))))

def hashes(key, mask):
    for x in count(1):
        t = f"{key}{x}"
        h = md5(t.encode()).digest()
        if is_valid(h, mask):
            yield x

mask = bytes.fromhex("ffffff0000000000")

key = sys.stdin.readline().rstrip()

print(next(hashes(key, mask)))

    
