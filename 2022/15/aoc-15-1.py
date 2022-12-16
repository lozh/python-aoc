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
def sensor_cover_for_y(sensor_info, y):
    sensor = sensor_info["sensor"]
    beacon = sensor_info["beacon"]
    size = manhattan(sensor, beacon)
    sx, sy = sensor
    ydist = manhattan(sensor, (sx, y))
    if ydist <= size:
        return (sx + ydist - size, sx - ydist + size)

# turn a list of ranges in to a list of disjoint ranges
# If ranges overlap they can be merged
def consolidate_ranges(ranges):
    ranges = sorted(ranges)
    cur = None
    for r in ranges:
        if cur == None:
            cur = r
        else:
            # print(f"{cur}, {r}")
            if r[0] <= cur[1]:
                # ranges overlap
                cur = (cur[0], max(cur[1], r[1]))
            else:
                yield cur
                cur = None
    if cur != None:
        yield cur

def pos_count_not_beacon(ranges, beacons):
    size = 0
    for r in ranges:
        size += r[1] - r[0] + 1
        size -= sum(1 for x, _ in beacons if x >= r[0] and x <= r[1])
    return size
    
y = 2000000
# y = 10

sensor_info = list(map(parse_line, sys.stdin))
y_ranges = (sensor_cover_for_y(s, y) for s in sensor_info)
y_ranges = filter(None, y_ranges)
y_ranges = consolidate_ranges(y_ranges)
# just need to remove beacons from the sensor ranges
beacons = { s["beacon"] for s in sensor_info if s["beacon"][1] == y}
ans = pos_count_not_beacon(y_ranges, beacons)
print(ans)


