#!/usr/bin/env python3
import sys
from dataclasses import dataclass

@dataclass(frozen=True)
class Direction:
    x: int
    y: int

north = Direction(0, -1)
east = Direction(1, 0)
south = Direction(0, 1)
west = Direction(-1, 0)

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

def illumination_count(layout, initial_beam, width, height):
    light_trails = set()
    light_heads = {initial_beam}
    while light_heads:
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
                    next_heads.add(beam.next(north))
                    next_heads.add(beam.next(south))
                case ('-', 0, 1) | ('-', 0, -1):
                    next_heads.add(beam.next(west))
                    next_heads.add(beam.next(east))
                case ('-', 1, 0) | ('-', -1, 0):
                    next_heads.add(beam.next())
                case '\\', 0, 1:
                    next_heads.add(beam.next(east))
                case '\\', 0, -1:
                    next_heads.add(beam.next(west))
                case '\\', 1, 0:
                    next_heads.add(beam.next(south))
                case '\\', -1, 0:
                    next_heads.add(beam.next(north))
                case '/', 0, 1:
                    next_heads.add(beam.next(west))
                case '/', 0, -1:
                    next_heads.add(beam.next(east))
                case '/', 1, 0:
                    next_heads.add(beam.next(north))
                case '/', -1, 0:
                    next_heads.add(beam.next(south))
                case _:
                    raise Exception(f"broken {tile}, {beam}")

        light_heads = next_heads

    illuminated = {beam.pos for beam in light_trails}
    return len(illuminated)

lines = map(str.rstrip, sys.stdin)
layout = list(map(list, lines))
width = len(layout[0])
height = len(layout)

ib_east = [Beam(Pos(0, j), Direction(1, 0)) for j in range(height)]
ib_west = [Beam(Pos(width - 1, j), Direction(-1, 0)) for j in range(height)]
ib_north = [Beam(Pos(i, height - 1), Direction(0, -1)) for i in range(width)]
ib_south = [Beam(Pos(i, 0), Direction(0, 1)) for i in range(width)]

initial_beams = ib_east + ib_west + ib_north + ib_south

print(max(map(lambda ib: illumination_count(layout, ib, width, height), initial_beams)))
