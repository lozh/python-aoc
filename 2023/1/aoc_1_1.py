#!/usr/bin/env python3

import itertools
import sys
import re

def line_to_number(line):
    m1 = re.search(r"\d", line)
    m2 = re.search(r"\d", line[::-1])
    return int(m1[0] + m2[0])

stdin = map(str.rstrip, sys.stdin)

print(sum(map(line_to_number, stdin)))
