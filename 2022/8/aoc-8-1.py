#!/usr/bin/env /usr/bin/python3

import sys

# return list of lists of numbers
def parse_input(stdin):
    for line in stdin:
        yield list(map(int, line))


def ranges(x, y, maxx, maxy):
    yield map(lambda z: ((x, y), (z, y)), range(0, x))
    yield map(lambda z: ((x, y), (z, y)), range(x + 1, maxx))
    yield map(lambda z: ((x, y), (x, z)), range(0, y))
    yield map(lambda z: ((x, y), (x, z)), range(y + 1, maxy))

debug = {}
# trees
def is_visible(trees, x, y):
    for r in ranges(x, y, len(trees[0]), len(trees)):
        visible = True
        for ((x1, y1), (x2, y2)) in r:
            if (x, y) in debug:
                print(f"(({x1}, {y1}), ({x2}, {y2})): ({trees[x1][y1]}, {trees[x2][y2]})")
            if trees[x1][y1] <= trees[x2][y2]:
                if (x, y) in debug:
                    print("False")
                visible = False
                break
        if visible:
            return True
    return False
    
stdin = sys.stdin.read().splitlines()

trees = list(parse_input(stdin))

visible_count = 0

for x in range(0, len(trees[0])):
    for y in range(0, len(trees)):
        if is_visible(trees, x, y):
            print(f"{x}, {y}, {trees[x][y]}, True")
            visible_count = visible_count + 1
        else:
            print(f"{x}, {y}, {trees[x][y]}, False")
print(visible_count)
               
