#!/usr/bin/env /usr/bin/python3

import sys
import itertools
from itertools import islice, tee
vowels = {"a", "e", "i", "o", "u"}
bad = {("a", "b"), ("c", "d"), ("p", "q"), ("x", "y")}

def iter_len(i):
    return sum(1 for _ in i)

# This is in itertools in Python 3.10
def pairwise(i):
    a, b = tee(i)
    next(b, None)
    return zip(a, b)

def string_has_n_from_set(n, s, set):
    vowels = (c for c in s if c in set)
    return n == iter_len(islice(vowels, n))

def string_has_3_vowels(s):
    return string_has_n_from_set(3, s, vowels)

def is_double_letter(pair):
    return pair[0] == pair[1]

def string_has_double_letter(s):
    return any(is_double_letter(x) for x in  pairwise(s))

def string_is_bad(s):
    return any(x in bad for x in pairwise(s))

def nice(s):
    return string_has_3_vowels(s) and string_has_double_letter(s) and not string_is_bad(s)

print(iter_len(s for s in map(str.rstrip, sys.stdin) if nice(s)))

