#!/usr/bin/env python3

import sys
import re
from sympy import symbols, solve

def parse(line):
    m = re.match(r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)", line)
    return int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5]), int(m[6])

lines = map(str.rstrip, sys.stdin)
x1, y1, z1, vx1, vy1, vz1 = parse(next(lines))
x2, y2, z2, vx2, vy2, vz2 = parse(next(lines))
x3, y3, z3, vx3, vy3, vz3 = parse(next(lines))

# rock parameters
x = symbols('x')
y = symbols('y')
z = symbols('z')
vx = symbols('vx')
vy = symbols('vy')
vz = symbols('vz')
# let t1, t2, t3 be the times of the intercepts of the first three hailstones
# Then x1 + vx1 * t1 = x * vx * t1 etc
t1 = symbols('t1')
t2 = symbols('t2')
t3 = symbols('t3')

equations = [
    x1 + vx1 * t1 - (x + vx * t1),
    y1 + vy1 * t1 - (y + vy * t1),
    z1 + vz1 * t1 - (z + vz * t1),
    x2 + vx2 * t2 - (x + vx * t2),
    y2 + vy2 * t2 - (y + vy * t2),
    z2 + vz2 * t2 - (z + vz * t2),
    x3 + vx3 * t3 - (x + vx * t3),
    y3 + vy3 * t3 - (y + vy * t3),
    z3 + vz3 * t3 - (z + vz * t3),
]

solution = solve(equations, [x, y, z, vx, vy, vz, t1, t2, t3], dict=True)[0]
print(solution[x] + solution[y] + solution[z])
