#!/usr/bin/env /usr/bin/python3

import sys

# parse a string literal into a string
def parse(s):
    quote, *s = s
    ret = ""
    assert(quote == "\"")
    while True:
        c, *s = s
        if c == '"':
            return ret
        if c == "\\":
            c, *s = s
            if c == 'x':
                h1, h2, *s = s
                c = chr(bytes.fromhex(h1 + h2)[0])
        ret += c

diffs = (len(s) - len(parse(s)) for s in map(str.rstrip, sys.stdin))
print(sum(diffs))
