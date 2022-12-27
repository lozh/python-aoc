#!/usr/bin/env /usr/bin/python3

import sys
from collections import Counter
from itertools import repeat

dir_lists = [
    # NW, N, NE
    [(-1, -1), (0, -1), (1, -1)],
    # SW, S, SE
    [(-1, 1), (0, 1), (1, 1)],
    # NW, W, SW
    [(-1, -1), (-1, 0), (-1, 1)],
    # NE, E, SE
    [(1, -1), (1, 0), (1, 1)]
]

def read_elves(lines):
    elves = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                elves.add((x, y))
    return elves

def any_neighbours(pos, elves):
    x, y = pos
    for i in range(x - 1, x + 2):
        for j in range (y - 1, y + 2):
            if i == x and j == y:
                continue
            if (i, j) in elves:
                return True
    return False

def any_neighbours_in_dirs(pos, elves, dir_list):
    for dir in dir_list:
        n = pos[0] + dir[0], pos[1] + dir[1]
        if n in elves:
            return True
    return False

def print_elves(elves):
    min_x = min(x for x, _ in elves)
    max_x = max(x for x, _ in elves) + 1
    min_y = min(y for _, y in elves)
    max_y = max(y for _, y in elves) + 1

    disp = []
    for i in range(min_y, max_y):
        disp.append(list(repeat('.', max_x - min_x)))

    for x, y in elves:
        disp[y - min_y][x - min_x] = '#'

    for l in disp:
        print("".join(l))

def evolve(elves, dir_lists):
    proposals = {}
    dests = Counter()
    for elf in elves:
        if not any_neighbours(elf, elves):
            continue
        for dir_list in dir_lists:
            if not any_neighbours_in_dirs(elf, elves, dir_list):
                dest = elf[0] + dir_list[1][0], elf[1] + dir_list[1][1]
                proposals[elf] = dest
                dests[dest] += 1
                break

    for elf in proposals:
        if dests[proposals[elf]] == 1:
            elves.remove(elf)
            elves.add(proposals[elf])

    return elves

def simulate(elves, dir_lists, turns):
    for _ in range(turns):
        elves = evolve(elves, dir_lists)
        front = dir_lists[0]
        del dir_lists[0]
        dir_lists.append(front)
    return elves

def measure(elves):
    min_x = min(x for x, _ in elves)
    max_x = max(x for x, _ in elves) + 1
    min_y = min(y for _, y in elves)
    max_y = max(y for _, y in elves) + 1
    return (max_x - min_x) * (max_y - min_y) - sum(1 for _ in elves)

elves = read_elves(map(str.rstrip, sys.stdin))
elves = simulate(elves, dir_lists, 10)
print(measure(elves))


