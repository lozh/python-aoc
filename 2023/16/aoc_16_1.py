#!/usr/bin/env python3

import sys

from dataclasses import dataclass

@dataclass(frozen=True)
class Direction:
    x: int
    y: int

@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def next(self, direction):
        return Pos(self.x + direction.x, self.y + direction.y)
    
@dataclass(frozen=True)
class Beam:
    pos: Pos
    direction: Direction

    def next(self, dir = None):
        if not dir:
            dir = self.direction
        return Beam(self.pos.next(dir), dir)

def in_bounds(width, height, pos):
    return pos.x >= 0 and pos.x < width and pos.y >= 0 and pos.y < height
    
light_heads = {Beam(Pos(0, 0), Direction(1, 0))}
light_trails = set()

lines = map(str.rstrip, sys.stdin)
layout = list(map(list, lines))
width = len(layout[0])
height = len(layout)

while light_heads:
    # print(light_heads)
    next_heads = set()
    for beam in light_heads:
        if beam in light_trails or not in_bounds(width, height, beam.pos):
            continue
        
        light_trails.add(beam)
        tile = layout[beam.pos.y][beam.pos.x]
        match tile, beam.direction.x, beam.direction.y:
            case '.', _, _:
                next_heads.add(beam.next())
            case ('|', 0, 1) | ('|', 0, -1):
                next_heads.add(beam.next())
            case ('|', 1, 0) | ('|', -1, 0):
                next_heads.add(beam.next(Direction(0, 1)))
                next_heads.add(beam.next(Direction(0, -1)))
            case ('-', 0, 1) | ('-', 0, -1):
                next_heads.add(beam.next(Direction(1, 0)))
                next_heads.add(beam.next(Direction(-1, 0)))
            case ('-', 1, 0) | ('-', -1, 0):
                next_heads.add(beam.next())
            case '\\', 0, 1:
                next_heads.add(beam.next(Direction(1, 0)))
            case '\\', 0, -1:
                next_heads.add(beam.next(Direction(-1, 0)))
            case '\\', 1, 0:
                next_heads.add(beam.next(Direction(0, 1)))
            case '\\', -1, 0:
                next_heads.add(beam.next(Direction(0, -1)))
            case '/', 0, 1:
                next_heads.add(beam.next(Direction(-1, 0)))
            case '/', 0, -1:
                next_heads.add(beam.next(Direction(1, 0)))
            case '/', 1, 0:
                next_heads.add(beam.next(Direction(0, -1)))
            case '/', -1, 0:
                next_heads.add(beam.next(Direction(0, 1)))
            case _:
                raise Exception(f"broken {tile}, {beam}")

    light_heads = next_heads

illuminated = {beam.pos for beam in light_trails}
print(len(illuminated))
