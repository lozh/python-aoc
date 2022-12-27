#!/usr/bin/env /usr/bin/python3

import sys
from math import copysign

def parse_line(line):
    x, y = line.split(" ")
    return (x, int(y))

def parse_lines(lines):
    return map(parse_line, lines)

def apply_move(game, move, vecs, tails):
    direction, count = move
    vx, vy = vecs[direction]
    for i in range(count):
        hx, hy = game['H']
        hx, hy = hx + vx, hy + vy
        game['H'] = (hx, hy)
        tx, ty = game['T']
        dx, dy = hx - tx, hy - ty
        if abs(dx) > 1 or abs(dy) > 1:
            # tail needs to move
            if abs(dx) > 0:
                tx += int(copysign(1, dx))
            if abs(dy) > 0:
                ty += int(copysign(1, dy))
        tail = (tx, ty)
        game['T'] = tail
        if not tail in tails:
            tails.add(tail)
    return (game, tails)

game = {'H': (0, 0), 'T': (0, 0)}
vecs = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}
tails = {(0,0)}

for move in parse_lines(map(str.rstrip, sys.stdin)):
    game, tails = apply_move(game, move, vecs, tails)

print(len(tails))
