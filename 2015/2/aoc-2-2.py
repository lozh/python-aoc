#!/usr/bin/env /usr/bin/python3

import sys
import re
import functools
from functools import reduce
import operator
from operator import mul

line_re = re.compile("^(\d+)x(\d+)x(\d+)$")
def parse_line(line):
    m = line_re.match(line)
    return int(m.group(1)), int(m.group(2)), int(m.group(3))

def ribbon_needed(package):
    p = sorted(package)
    return p[0] * 2 + p[1] * 2 + reduce(mul,p)

packages = map(parse_line, sys.stdin)
print(sum(map(ribbon_needed, packages)))

