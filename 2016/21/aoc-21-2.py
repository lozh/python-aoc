#!/usr/bin/env /usr/bin/python3

import sys
import re
from functools import partial
from dataclasses import dataclass

# Now funcs need to do the inverse

def swap_pos(src, dst, s):
    chars = [c for c in s]
    chars[src], chars[dst] = chars[dst], chars[src]
    return "".join(chars)

def swap_chars(src, dst, s):
    ss = s.index(src)
    dd = s.index(dst)
    return swap_pos(ss, dd, s)

def rotate_left(step, s):
    step = step % len(s)
    return s[step:] + s[:step]

def rotate_right(step, s):
    step = step % len(s)
    return s[-step:] + s[:-step]

def rotate_letter(l, s):
    i = s.index(l)
    if i >= 4:
        i += 1
    return rotate_right(i + 1, s)

def reverse_rotate_letter(l, s):
    for i in range(len(s)):
        if s == rotate_letter(l, rotate_left(i, s)):
            return rotate_left(i, s)

def reverse(start, end, s):
    return s[:start] + "".join(reversed(s[start:end+1])) + s[end+1:]

def move_pos(src, dst, s):
    chars = [c for c in s]
    c = chars[src]
    del chars[src]
    chars.insert(dst, c)
    return "".join(chars)

@dataclass
class Term:
    # An re that matches the term
    parse_re: object
    # a function that takes a match and returns a function to scramble a string
    scramble_func: object

terms = [
    Term(
        parse_re = re.compile("^swap position (\d+) with position (\d+)$"),
        scramble_func = lambda m: partial(swap_pos, int(m.group(1)), int(m.group(2)))
    ),
    Term(
        parse_re = re.compile("^swap letter ([a-z]) with letter ([a-z])$"),
        scramble_func = lambda m: partial(swap_chars, m.group(1), m.group(2))
    ),
    Term(
        parse_re = re.compile("^rotate left (\d+) steps?$"),
        scramble_func = lambda m: partial(rotate_right, int(m.group(1)))
    ),
    Term(
        parse_re = re.compile("^rotate right (\d+) steps?$"),
        scramble_func = lambda m: partial(rotate_left, int(m.group(1)))
    ),
    Term(
        parse_re = re.compile("^rotate based on position of letter ([a-z])$"),
        scramble_func = lambda m: partial(reverse_rotate_letter, m.group(1))
    ),
    Term(
        parse_re = re.compile("^reverse positions (\d+) through (\d+)$"),
        scramble_func = lambda m:partial(reverse, int(m.group(1)), int(m.group(2)))
    ),
    Term(
        parse_re = re.compile("^move position (\d+) to position (\d+)$"),
        scramble_func = lambda m: partial(move_pos, int(m.group(2)), int(m.group(1)))
    )
]
s = "fbgdceah"

for line in reversed(sys.stdin.readlines()):
    matched = False
    for term in terms:
        if m:= term.parse_re.match(line):
            matched = True
            f = term.scramble_func(m)
            s = f(s)
            break
    if not matched:
        raise Exception(f"Could not parse line: {line}")

print(s)
