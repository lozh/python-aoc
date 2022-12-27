#!/usr/bin/env /usr/bin/python3

import sys

# return list of lists of numbers
def parse_input(stdin):
    for line in stdin:
        yield list(map(int, line))


def ranges(x, y, maxx, maxy):
    yield map(lambda z: ((x, y), (z, y)), range(x))
    yield map(lambda z: ((x, y), (z, y)), range(x + 1, maxx))
    yield map(lambda z: ((x, y), (x, z)), range(y))
    yield map(lambda z: ((x, y), (x, z)), range(y + 1, maxy))

# trees
def is_visible(trees, x, y):
    for r in ranges(x, y, len(trees[0]), len(trees)):
        visible = True
        for ((x1, y1), (x2, y2)) in r:
            if trees[x1][y1] <= trees[x2][y2]:
                visible = False
                break
        if visible:
            return True
    return False
    
trees = list(parse_input(map(str.rstrip, sys.stdin)))

visible_count = 0

for x in range(len(trees[0])):
    for y in range(len(trees)):
        if is_visible(trees, x, y):
            visible_count += 1

print(visible_count)
               
