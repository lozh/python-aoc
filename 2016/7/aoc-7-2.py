#!/usr/bin/env /usr/bin/python3

import sys
from itertools import product

def is_aba(s):
    return s[0] == s[2] and s[0] != s[1]

def aba_eq_bab(a, b):
    return a[0] == b[1] and a[1] == b[0]

def supports_ssl(s):
    abas = set()
    babs = set()
    in_bracket = False
    for i in range(len(s) - 2):
        if s[i] == '[':
            in_bracket = True
        elif s[i] == ']':
            in_bracket = False
        elif is_aba(s[i:i + 3]):
            if in_bracket:
                # only need to remember two chars
                babs.add(s[i:i + 2])
            else:
                abas.add(s[i:i + 2])
    return any(aba_eq_bab(a, b) for a, b in product(abas, babs))

print(sum(1 for line in map(str.rstrip, sys.stdin) if supports_ssl(line)))

