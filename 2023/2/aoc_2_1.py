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

def draw_compatible(draw, base):
    return all(d <= b for (d, b) in zip(draw, base))

def game_compatible(game, base):
    return all(draw_compatible(draw, base) for draw in game.draws)

stdin = map(str.rstrip, sys.stdin)
games = map(parse, stdin)
print(sum(g.no for g in games if game_compatible(g, elf_draw)))

