#!/usr/bin/env /usr/bin/python3

import sys
import re

line_re = re.compile("^(\d+)x(\d+)x(\d+)$")
def parse_line(line):
    m = line_re.match(line)
    return int(m.group(1)), int(m.group(2)), int(m.group(3))

def paper_needed(package):
    p = sorted(package)
    return p[0] * p[1] * 3 + p[0] * p[2] * 2 + p[1] * p[2] * 2
                                                    
packages = map(parse_line, sys.stdin)
print(sum(map(paper_needed, packages)))

