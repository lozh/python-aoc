#!/usr/bin/env python3

import itertools
import sys
import re

forward = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

backward = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 0,
    "eno": 1,
    "owt": 2,
    "eerht": 3,
    "ruof": 4,
    "evif": 5,
    "xis": 6,
    "neves": 7,
    "thgie": 8,
    "enin": 9
}

def line_to_number(line):
    m1 = re.search(r"\d|one|two|three|four|five|six|seven|eight|nine", line)
    m2 = re.search(r"\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin", line[::-1])
    d1 = forward[m1[0]]
    d2 = backward[m2[0]]
    return 10 * d1 + d2

stdin = map(str.rstrip, sys.stdin)

print(sum(map(line_to_number, stdin)))
