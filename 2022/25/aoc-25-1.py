#!/usr/bin/env /usr/bin/python3

import sys

s_val = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}

def snafu_to_d(s):
    base = 5
    p = 0
    ret = 0
    while True:
        *s, c = s
        ret = ret + pow(base, p) * s_val[c]
        p += 1
        if not s:
            return ret

d_val = {0: (0, '0'), 1: (1, '1'), 2: (2, '2'), 3: (-2, '='), 4: (-1, '-')}

def d_to_snafu(d):
    base = 5
    p = 1
    ret = []
    while True:
        pent = d % base
        x, c = d_val[pent]
        d = (d - x) // base
        ret.append(c)
        if d == 0:
            return "".join(reversed(ret))

d_sum = sum(map(snafu_to_d, map(str.rstrip, sys.stdin)))
print(d_to_snafu(d_sum))

