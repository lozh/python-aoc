#!/usr/bin/env /usr/bin/python3

import sys
import re

line_re = re.compile("^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")

def parse_line(line):
    m = line_re.match(line)
    if (m):
        return {
            "sensor": (int(m.group(1)), int(m.group(2))),
            "beacon": (int(m.group(3)), int(m.group(4)))
        }
    else:
        print(f"Cound not parse line: {line}")
        raise

def tuple_map(f, x, y):
    return tuple(f(a, b) for (a, b) in zip(x, y))

def manhattan(pos1, pos2):
    return sum(tuple_map(lambda x, y: abs(x - y), pos1, pos2))

# What is the range of cover on line y for sensor, given that it extends
# as far as beacon
def sensor_cover_for_y(sensor_info, y, bound):
    sensor = sensor_info["sensor"]
    beacon = sensor_info["beacon"]
    size = manhattan(sensor, beacon)
    sx, sy = sensor
    ydist = manhattan(sensor, (sx, y))
    if ydist <= size:
        bs, be = bound
        rs = sx + ydist - size
        re = sx - ydist + size
        if rs < bs:
            rs = bs
        if re > be:
            re = be
        if not (rs > be or re < bs):
            return (rs, re)

# turn a list of ranges in to a list of disjoint ranges
# If ranges overlap they can be merged
def consolidate_ranges(ranges):
    ranges = sorted(ranges)
    cur = None
    for r in ranges:
        if cur == None:
            cur = r
        else:
            if r[0] <= cur[1]:
                # ranges overlap
                cur = (cur[0], max(cur[1], r[1]))
            else:
                yield cur
                cur = None
    if cur != None:
        yield cur

def bound_range(range, bound):
    rx, ry = range
    bx, by = bound
    if rx < bx:
        rx = bx
    if ry > by:
        ry = by
    return (rx, ry)

# find a square not covered by a sensor
def solve(sensor_info, size):
    bound = (0, size)
    for y in range(size + 1):
        y_ranges = (sensor_cover_for_y(s, y, bound) for s in sensor_info)
        y_ranges = filter(None, y_ranges)
        y_ranges = consolidate_ranges(y_ranges)
        # y_ranges = map(lambda r: bound_range(r, bound), y_ranges)
        r, *_ = y_ranges
        if r[0] != 0:
            return (0, y)
        if r[1] != size:
            return (r[1] + 1, y)

def tuning_frequency(pos):
    return pos[0] * 4000000 + pos[1]
    
size = 4000000
# size = 20

sensor_info = list(map(parse_line, sys.stdin))
ans = solve(sensor_info, size)
print(tuning_frequency(ans))



