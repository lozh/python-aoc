#!/usr/bin/env /usr/bin/python3

import sys
import re
import collections
from collections import Counter
import itertools
from itertools import chain

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

coord_re = re.compile("^(\d+),(\d+),(\d+)$")

def parse_line(line):
    m = coord_re.match(line)
    return int(m.group(1)), int(m.group(2)), int(m.group(3))

cubes = map(parse_line, sys.stdin)
cube_faces = chain.from_iterable(map(faces, cubes))
face_counts = Counter(cube_faces)
unique_face_counts = sum(1 for v in face_counts.values() if v == 1)
print(unique_face_counts)
