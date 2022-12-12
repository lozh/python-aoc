#!/usr/bin/env /usr/bin/python3

import itertools
from itertools import groupby
import sys

def elf_to_cal(cal_list):
    return sum(cal_list)

def input_to_elves(lines):
    raw = groupby(lines, lambda x: x == "")
    for key, group in raw:
        if not key:
            yield map(int, group)

stdin = map(str.rstrip, sys.stdin)

elves = input_to_elves(stdin)
sorted_elves = sorted(map(elf_to_cal, elves), reverse = True)

print(sum(sorted_elves[:3]))




    
