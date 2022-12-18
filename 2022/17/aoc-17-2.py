#!/usr/bin/env /usr/bin/python3

import sys
import itertools
from itertools import cycle, count

shapes = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)]
]

offsets = { '>':(1, 0), '<':(-1, 0) }
down = (0, -1)

def height(shape):
    return max(y for _, y in shape) + 1

def add_pair(x, y):
    return (x[0] + y[0], x[1] + y[1])

def can_move(rock, pos, offset, world):
    for r in rock:
        x, y = add_pair(add_pair(pos, r), offset)
        if x < 0:
            return False
        if x > 6:
            return False
        if y < 0:
            return False
        if (x, y) in world:
            return False
    return True

def is_line(world, y):
    for x in range(7):
        if (x, y) not in world:
            return False
    return True

def simulate(rocks, jets):
    rocks = cycle(enumerate(shapes))
    jets = cycle(enumerate(jets))
    world = set()
    top = 0
    j_no = 0
    for rock_no in count():
        r_no, rock = next(rocks)
        pos = (2, top + 3)
        # simulate rock
        while True:
            # apply jet
            j_no, jet = next(jets)
            offset = offsets[jet]
            if can_move(rock, pos, offset, world):
                pos = add_pair(pos, offset)
            if can_move(rock, pos, down, world):
                pos = add_pair(pos, down)
            else:
                break
        # Add rock to world
        for r in rock:
            world.add(add_pair(pos, r))
        top = max(top, pos[1] + height(rock))
        yield ((r_no, j_no), (rock_no, top))

def find_cycle(shapes, jets, repeat_count):
    seen = {}
    cycle = []
    top_diff = 0
    r_start = 0
    t_start = 0
    rock_diff = 0
    scan_count = 0
    # have we seen a repeat?
    scanning = False
    sim = simulate(shapes, iter(jets))
    for (key, stat) in sim:
        if scanning:
            if key in seen:
                sr, st = seen[key]
                if stat[0] - sr != rock_diff or stat[1] - st != top_diff:
                    # different cycle, restart
                    cycle = [0]
                    r_start, t_start = stat
                    rock_diff = r_start - sr
                    top_diff = t_start - st
                    scan_count = repeat_count * rock_diff
                else:
                    scan_count -= 1
                    cycle.append((st - t_start) % top_diff)
                    if scan_count == 0:
                        # we return more copies of the cycle than we need to,
                        # but it doesn't matter
                        return (r_start, t_start, rock_diff, top_diff, cycle)
            else:
                scanning = False
                cycle = []
        else:
            if key in seen:
                cycle = [0]
                sr, st = seen[key]
                scanning = True
                r_start, t_start = stat
                rock_diff = r_start - sr
                top_diff = t_start - st
                scan_count = repeat_count * rock_diff
        seen[key] = stat
    

jets = sys.stdin.readline().strip()

rock_count = 1000000000000

r_start, t_start, r_diff, t_diff, seen = find_cycle(shapes, jets, 10)
# height to start of cycle
height = t_start
# number of equal stacks before one more stack would take us past rock_count
stacks = (rock_count - r_start) // r_diff
height += stacks * t_diff
# number of additional rocks to finish
rocks_left = ((rock_count - r_start) % r_diff) - 1
height += seen[rocks_left]
print(height)
