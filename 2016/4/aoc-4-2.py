#!/usr/bin/env /usr/bin/python3

import sys
import re
from collections import Counter

line_re = re.compile("^([a-z-]+)(\d+)\[([a-z]{5})\]$")
# return (letters, sector, checkum)
def parse_line(line):
    if m := line_re.match(line):
        letters = m.group(1)
        sector = int(m.group(2))
        checksum = m.group(3)
        return letters, sector, checksum
    else:
        raise Exception(f"{line}")

def checksum(letters):
    letters = [l for l in letters if l != '-']
    letters.sort()
    c = Counter(letters)
    return "".join(l for l, _ in c.most_common(5))

def decrypt(letters, sector):
    ret = []
    for l in letters:
        if l == '-':
            ret.append(' ')
        else:
            c = (ord(l) - ord('a') + sector) % 26
            ret.append(chr(c + ord('a')))
    return "".join(ret)

iput = map(parse_line, sys.stdin)
for letters, sector, cs in iput:
    if checksum(letters) == cs:
        if decrypt(letters, sector) == "northpole object storage ":
            print(sector)
