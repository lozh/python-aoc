#!/usr/bin/env /usr/bin/python3

import sys
from math import copysign

def parse_line(line):
    x, y = line.split(" ")
    return (x, int(y))

def parse_lines(stdin):
    return map(parse_line, stdin)

def move_knot(h, t):
    hx, hy = h
    tx, ty = t
    dx, dy = hx - tx, hy - ty
    if abs(dx) > 1 or abs(dy) > 1:
        if abs(dx) > 0:
            tx += int(copysign(1, dx))
        if abs(dy) > 0:
            ty += int(copysign(1, dy))
    return tx, ty

def apply_move(game, move, vecs, tails):
    direction, count = move
    vx, vy = vecs[direction]
    for i in range(count):
        hx, hy = game[0]
        hx, hy = hx + vx, hy + vy
        game[0] = (hx, hy)
        for j in range(1, knot_count):
            game[j] = move_knot(game[j - 1], game[j])

        tail = game[knot_count - 1]
        if not tail in tails:
            tails.add(tail)
    return (game, tails)

knot_count = 10

# initialize with all knots at (0, 0)
# game is dict of knot# -> (knot_x, knot_y)
game = dict(map(lambda x: (x, (0, 0)), range(knot_count)))

vecs = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}

# unique positins tail has visited
tails = {(0,0)}

for move in parse_lines(map(str.rstrip, sys.stdin)):
    game, tails = apply_move(game, move, vecs, tails)

print(len(tails))
