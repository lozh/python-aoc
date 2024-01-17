#!/usr/bin/env python3
import sys

def get_groups(arrangement):
    c = 0
    i = False
    for x in arrangement:
        if x == '.':
            if i:
                yield c
                i = False
                c = 0
        else:
            c += 1
            i = True
    if c > 0:
        yield c

def is_valid(arrangement, groups):
    return list(get_groups(arrangement)) == groups

def permute_r(pattern, groups, missing, slots, spring_count):
    if missing == 0:
        yield pattern.replace('?', '.')
    else:
        if missing > 0:
            yield from permute_r(pattern.replace('?', '#', 1), groups, missing - 1, slots - 1, spring_count)
        if slots > missing:
            yield from permute_r(pattern.replace('?', '.', 1), groups, missing, slots - 1, spring_count)

def permute(pattern, groups):
    spring_count = sum(groups)
    slots = sum(1 for x in pattern if x == '?')
    missing = spring_count - sum(1 for x in pattern if x == '#')
    yield from permute_r(pattern, groups, missing, slots, spring_count)

def parse(line):
    pattern, groups = line.split()
    return (pattern, list(map(int, groups.split(","))))

def count_arrangements(pattern, groups):
    return sum(1 for x in permute(pattern, groups) if is_valid(x, groups))

stdin = map(str.rstrip, sys.stdin)

print(sum(count_arrangements(p, g) for (p, g) in map(parse, stdin)))
