#!/usr/bin/env /usr/bin/python3

import itertools
import sys

def elf_to_cal(cal_list):
    return sum(cal_list)

def input_to_elves(lines):
    raw = itertools.groupby(lines, lambda x: x == "")
    for key, group in raw:
        if not key:
            yield map(int, group)

stdin = sys.stdin.read().splitlines()

elves = input_to_elves(stdin)

print(max(map(elf_to_cal, elves)))





    
