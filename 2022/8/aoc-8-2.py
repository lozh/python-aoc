#!/usr/bin/env /usr/bin/python3

import sys
import functools

# return list of lists of numbers
def parse_input(stdin):
    for line in stdin:
        yield list(map(int, line))


def ranges(x, y, maxx, maxy):
    yield map(lambda z: (z, y), reversed(range(0, x)))
    yield map(lambda z: (z, y), range(x + 1, maxx))
    yield map(lambda z: (x, z), reversed(range(0, y)))
    yield map(lambda z: (x, z), range(y + 1, maxy))

debug = {}
# trees
def is_visible(trees, x, y):
    for r in ranges(x, y, len(trees[0]), len(trees)):
        visible = True
        for (x2, y2) in r:
            if (x, y) in debug:
                print(f"(({x1}, {y1}), ({x2}, {y2})): ({trees[x1][y1]}, {trees[x2][y2]})")
            if trees[x][y] <= trees[x2][y2]:
                if (x, y) in debug:
                    print("False")
                visible = False
                break
        if visible:
            return True
    return False

def score(trees, x, y, r):
    score = 0
    if (x, y) in debug:
        print(f"{x}, {y}, {trees[x][y]}")
    for (x2, y2) in r:
        if (x, y) in debug:
            print(f"{x}, {y}, {x2}, {y2}, {trees[x][y]}, {trees[x2][y2]}")
        score = score + 1
        if trees[x2][y2] >= trees[x][y]:
            break
    return score

def scenic_score(trees, x, y):
    rs = ranges(x, y, len(trees[0]), len(trees))
    range_scores = map(lambda r: score(trees, x, y, r), rs)
    s = functools.reduce(lambda x, y: x * y, range_scores, 1)
    if (x, y) in debug:
        print(f"{x}, {y} = {s}")
    return s

def scenic_scores(trees):
    for x in range(0, len(trees[0])):
        for y in range(0, len(trees)):
            yield scenic_score(trees, x, y)

stdin = sys.stdin.read().splitlines()

trees = list(parse_input(stdin))

print(max(scenic_scores(trees)))
               
