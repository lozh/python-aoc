#!/usr/bin/env /usr/bin/python3

import sys
import re
import collections
from collections import Counter
import itertools
from itertools import chain, product

# iterate faces as opposite corners ((x0, y0, z0), (x1, y1, z1)) with A0 <= A1
# of a 1x1x1 cube starting at coord = (x, y, z)
def faces(coord):
    x, y, z = coord
    yield (x, y, z), (x + 1, y + 1, z)
    yield (x, y, z), (x, y + 1, z + 1)
    yield (x, y, z), (x + 1, y, z + 1)
    yield (x + 1, y, z), (x + 1, y + 1, z + 1)
    yield (x, y + 1, z), (x + 1, y + 1, z + 1)
    yield (x, y, z + 1), (x + 1, y + 1, z + 1)

# Get a bounding box with a 
def bounding_box(cubes, gap):
    return (
        min((x for x, y, z in cubes)) - gap,
        min((y for x, y, z in cubes)) - gap,
        min((z for x, y, z in cubes)) - gap
    ), (
        max((x for x, y, z in cubes)) + gap + 1,
        max((y for x, y, z in cubes)) + gap + 1,
        max((z for x, y, z in cubes)) + gap + 1
    )

def in_bound(cube, bounds):
    x, y, z = cube
    (x0, y0, z0), (x1, y1, z1) = bounds
    return x >= x0 and x < x1 and y >= y0 and y < y1 and z >= z0 and z < z1

def neighbours(cube):
    x, y, z = cube
    yield (x - 1, y, z)
    yield (x + 1, y, z)
    yield (x, y - 1, z)
    yield (x, y + 1, z)
    yield (x, y, z - 1)
    yield (x, y, z + 1)
    
# Output all boxes that can be reached from start without
# going through an element in cubes or out of bounds
def fill(start, cubes, bounds):
    ret = {start}
    while True:
        new_cubes = set()
        for cube in ret:
            for n in neighbours(cube):
                if in_bound(n, bounds) and n not in ret and n not in cubes:
                    new_cubes.add(n)
        if not new_cubes:
            return ret
        ret.update(new_cubes)

def find_interior(cubes, exterior, bounds):
    ret = set()
    (x0, y0, z0), (x1, y1, z1) = bounds
    for c in product(range(x0, x1), range(y0, y1), range(z0, z1)):
        if c not in cubes and c not in exterior:
            ret.add(c)
    return ret

coord_re = re.compile("^(\d+),(\d+),(\d+)$")

def parse_line(line):
    m = coord_re.match(line)
    return int(m.group(1)), int(m.group(2)), int(m.group(3))

cubes = set(map(parse_line, sys.stdin))
bounds = bounding_box(cubes, 1)
exterior = fill(bounds[0], cubes, bounds)
interior = find_interior(cubes, exterior, bounds)
outside = cubes | interior
outside_faces = chain.from_iterable(map(faces, outside))
face_counts = Counter(outside_faces)
unique_face_counts = sum(1 for v in face_counts.values() if v == 1)
print(unique_face_counts)
