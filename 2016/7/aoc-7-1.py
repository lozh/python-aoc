#!/usr/bin/env /usr/bin/python3

import sys

# I think from the description
# that all [ will have a closing ]
# and also there will be no nesting
# check that here
def is_valid(s):
    in_bracket = False
    for c in s:
        if c == '[':
            if in_bracket:
                raise Exception("Nested Brackets")
            else:
                in_bracket = True
        elif c == ']':
            if not in_bracket:
                raise Exception("Close bracket without open")
            else:
                in_bracket = False
        else:
            if not c in "abcdefghijklmnopqrstuvwxyz":
                raise Exception("Unexpected char")
    if in_bracket:
        raise Exception("Unclosed bracket")
    return True

def is_abba(s):
    return s[0] == s[3] and s[1] == s[2] and s[0] != s[1]

def supports_tls(s):
    has_abba = False
    in_bracket = False
    for i in range(len(s) - 3):
        if s[i] == '[':
            in_bracket = True
        elif s[i] == ']':
            in_bracket = False
        elif is_abba(s[i:i + 4]):
            if in_bracket:
                return False
            else:
                has_abba = True
    return has_abba

print(sum(1 for line in map(str.rstrip, sys.stdin) if supports_tls(line)))

