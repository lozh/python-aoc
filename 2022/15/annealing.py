#!/usr/bin/env /usr/bin/python3

import sys
import re
import random
import math


size = 4000000
# size = 20


def tuple_map(f, x, y):
    return tuple(f(a, b) for (a, b) in zip(x, y))

def manhattan(pos1, pos2):
    return sum(tuple_map(lambda x, y: abs(x - y), pos1, pos2))

line_re = re.compile("^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")

def parse_line(line):
    m = line_re.match(line)

    if (m):
        sensor = (int(m.group(1)), int(m.group(2)))
        beacon = (int(m.group(3)), int(m.group(4)))
        size = manhattan(sensor, beacon)
        return {
            "sensor": sensor,
            "size": size
        }
    else:
        print(f"Cound not parse line: {line}")
        raise

# sum of distances to escape all sensors
# if this is 0, we're done
def cost(pos, sensors):
    dist = 0
    for s in sensors:
        m = manhattan(pos, s["sensor"])
        sz = s["size"]
        if m <= sz:
            dist += (sz - m + 1) * (sz - m + 1)
    return math.sqrt(dist)

def neighbours(pos, s):
    x, y = pos
    yield from ((x + i, y + j) for i in range(-s, s + 1) for j in range(-s, s + 1) if x + i >= 0 and x + i <= size and y + j >= 0 and y + j <= size)

def anneal(start, sensors):
    initial_temp = 90
    iterations = 100000

    current, current_cost = start, cost(start, sensors)
    best, best_cost = current, cost(current, sensors)

    for i in range(iterations):
        if best_cost == 0:
            return best, i
        t = initial_temp / float(1 + i)
        ns = list(neighbours(current, int(initial_temp - 0.01 * i)))
        n = random.choice(ns)
        n_cost = cost(n, sensors)
        cost_diff = best_cost - n_cost
        print(f"{best_cost}, {n_cost}, {n}, {best}, {cost_diff}, {t}")
        if cost_diff > 0:
            best, best_cost = n, n_cost
            current, current_cost  = n, n_cost
        else:
            if random.uniform(0, 1) < math.exp(-cost_diff / t):
                current, current_cost = n, n_cost
            else:
                print("not random")
    return best, iterations
    
start = (size // 2, size // 2)

sensors = list(map(parse_line, sys.stdin))
    
sol = anneal(start, sensors)
print(f"{sol} -> {cost(sol[0], sensors)}")



