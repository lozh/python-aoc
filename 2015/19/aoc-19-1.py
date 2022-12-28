#!/usr/bin/env /usr/bin/python3

import sys
import re

line_re = re.compile("^(\w+) => (\w+)$")

def parse_input(lines):
    subs = {}
    for line in lines:
        if not line:
            break

        m = line_re.match(line)
        f = m.group(1)
        if not f in subs:
            subs[f] = []

        subs[f].append(m.group(2))
    molecule = next(lines)
    return molecule, subs

def replacements(molecule, subs):
    for f in subs:
        i = molecule.find(f)
        while i >= 0:
            for r in subs[f]:
                yield molecule[:i] + r + molecule[i+len(f):]
            i = molecule.find(f, i + 1)

molecule, subs = parse_input(map(str.rstrip, sys.stdin))

s = set(replacements(molecule, subs))
print(len(s))

