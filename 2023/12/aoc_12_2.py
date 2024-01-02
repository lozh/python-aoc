#!/usr/bin/env python3

import sys
from itertools import repeat
from functools import lru_cache

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

def get_part_groups(pattern):
    c = 0
    i = False
    for x in pattern:
        match x:
            case '.':
                if i:
                    yield c
                    i = False
                    c = 0
            case '?':
                if i:
                    yield -c
                break
            case '#':
                c += 1
                i = True

def is_valid(arrangement, groups):
    return tuple(get_groups(arrangement)) == groups

# use to bail on permutation early
# if the pattern can never match the groups
# we just check from left to right until we hit the first ?
# whole groups before that need to match
# a part group must be less than or equal
def possible(pg, groups):
    for (x, y) in zip(pg, groups):
        if (x < 0 and (-x) > y) or (x > 0 and x != y):
            return False
    return True

# Remove any completely matched bits from the left
def chop(pattern, pg, groups):
    for i in pg:
        if i > 0:
            pg = pg[1:]
            groups = groups[1:]
            # 0 = searching for springs
            # 1 = in spring
            # 2 = after spring
            s = 0
            for j, c in enumerate(pattern):
                match c:
                    case '.':
                        if s == 1:
                            s = 2
                    case '#':
                        if s == 2:
                            pattern = pattern[j:]
                            break
                        s = 1
                    case '?':
                        if s != 2:
                            print("Broken")
                            return None
                        pattern = pattern[j:]
                        break
    return (pattern, pg, groups)

@lru_cache(maxsize = 1000000)
def count_perms(pattern, groups):
    spring_count = sum(groups)
    slots = sum(1 for x in pattern if x == '?')
    missing = spring_count - sum(1 for x in pattern if x == '#')
    pg = tuple(get_part_groups(pattern))
    if possible(pg, groups):
        if missing == 0:
            return 1 if is_valid(pattern.replace('?', '.'), groups) else 0
        if missing == slots:
            return 1 if is_valid(pattern.replace('?', '#'), groups) else 0

        (pattern, pg, groups) = chop(pattern, pg, groups)
        c = count_perms(pattern.replace('?', '#', 1), groups)
        if slots > missing:
            # no point trying a . if we're part way through filling a group
            if not pg or -pg[0] == groups[0]:
                c += count_perms(pattern.replace('?', '.', 1), groups)
        return c
    else:
        return 0


def parse(line):
    pattern, groups = line.split()
    pattern = '?'.join(repeat(pattern, 5))
    groups = ','.join(repeat(groups, 5))
    return (pattern, tuple(map(int, groups.split(","))))

stdin = map(str.rstrip, sys.stdin)

#for (p, g) in map(parse, stdin):
#    print(p, g)
#    print(count_perms(p, g))
#    print(count_perms.cache_info())
          
print(sum(count_perms(p, g) for (p, g) in map(parse, stdin)))

