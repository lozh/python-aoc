#! /usr/bin/env python3

from dataclasses import dataclass
from collections import namedtuple
import re
import sys
import itertools

Draw = namedtuple('Draw', 'r g b')

@dataclass
class Game:
    no: int
    draws: list[Draw]

elf_draw = Draw(12, 13, 14)

def parse_draw(draw):
    cubes = draw.split(", ")
    r = 0
    g = 0
    b = 0
    for cube in cubes:
        m = re.match(r"^(\d+) (red|green|blue)", cube)
        n = int(m[1])
        match m[2]:
            case "red":
                r = n
            case "green":
                g = n
            case "blue":
                b = n
    return Draw(r, g, b)

def parse(line):
    m = re.match(r"Game (\d+): (.*)$", line)
    no = int(m[1])
    rest = m[2]
    draws = []
    for draw in rest.split("; "):
        draws.append(parse_draw(draw))

    return Game(no = no, draws = draws)

def min_cubes(game):
    mr = max(r for (r, _, _) in game.draws)
    mg = max(g for (_, g, _) in game.draws)
    mb = max(b for (_, _, b) in game.draws)
    return Draw(mr, mg, mb)

stdin = map(str.rstrip, sys.stdin)
games = map(parse, stdin)

mins = map(min_cubes, games)

print(sum(r * g * b for (r, g, b) in mins))

