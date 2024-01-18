#!/usr/bin/env python3
import sys
import re
from dataclasses import dataclass

@dataclass
class Lens:
    label: str
    focal_length: int

@dataclass
class Box:
    lenses: list[Lens]

@dataclass
class Op:
    label: str
    remove: bool
    focal_length: int

boxes = {}

def hash(s):
    r = 0
    for c in s:
        r += ord(c)
        r *= 17
        r = r % 256
    return r

def parse(line):
    m = re.match(r"([a-z]+)([-=])(\d*)", line)
    if m[2] == "-":
        return Op(m[1], True, 0)
    else:
        return Op(m[1], False, int(m[3]))

line = next(sys.stdin).rstrip()
for op in map(parse, line.split(",")):
    box_id = hash(op.label)
    box = boxes.get(box_id, Box([]))
    if op.remove:
        box.lenses = [x for x in box.lenses if x.label != op.label]
    else:
        lens = next((lens for lens in box.lenses if lens.label == op.label), None)
        if lens:
            lens.focal_length = op.focal_length
        else:
            box.lenses.append(Lens(op.label, op.focal_length))

    boxes[box_id] = box

s = 0
for i, box in boxes.items():
    for j, lens in enumerate(box.lenses):
        s += (i + 1) * (j + 1) * lens.focal_length

print(s)
