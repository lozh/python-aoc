#!/usr/bin/env /usr/bin/python3

import sys
from json import loads

def sum_nums(j):
    if type(j) is int:
        return j
    t = 0
    if type(j) is dict:
        for v in j.values():
            t += sum_nums(v)
        return t
    if type(j) is list:
        for v in j:
            t += sum_nums(v)
        return t
    return 0

doc = loads(sys.stdin.read())

print(sum_nums(doc))
