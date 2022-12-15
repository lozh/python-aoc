#!/usr/bin/env /usr/bin/python3

import sys

q = "\""

def encode_char(c):
    if c == '"':
        return '\\"'
    if c == "\\":
        return "\\\\"
    return c

def encode(s):
    return q + "".join(map(encode_char, s)) + q

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

diffs = (len(encode(s)) - len(s) for s in map(str.rstrip, sys.stdin))
print(sum(diffs))
