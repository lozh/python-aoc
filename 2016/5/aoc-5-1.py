#!/usr/bin/env /usr/bin/python3

import sys
from hashlib import md5
from itertools import count, repeat, islice

def is_key(trial, mask):
    return all(a & b == 0 for a, b in zip(trial, mask))

def password(start, zerocount):
    mask = bytes.fromhex("".join(repeat("f", zerocount)) + "0" if zerocount % 2 == 1 else "")
    for i in count():
        h = md5(f"{start}{i}".encode()).digest()
        if is_key(h, mask):
            yield h.hex()[zerocount]

pass_len = 8
zero_count = 5
door = sys.stdin.readline().strip()
print("".join(islice(password(door, zero_count), pass_len)))
