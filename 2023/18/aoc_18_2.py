#!/usr/bin/env python3

import sys
import re

def parse(line):
    m = re.match(r"[UDLR] \d+ \(#([0-9a-f]{5})([0-3])\)", line)
    return (int(m[1], 16), dir_map[m[2]])
    return m

dir_map = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}

lines = map(str.rstrip, sys.stdin)
for (a, b) in map(parse, lines):
    print(f"{b} {a}")

                
    
