#!/usr/bin/env /usr/bin/python3

import sys
import math

def parse_line(line):
    x, y = line.split(" ")
    return (x, int(y))

def parse_lines(stdin):
    return map(parse_line, stdin)

def apply_move(game, move, vecs, tails):
    direction, count = move
    vx, vy = vecs[direction]
    for i in range(count):
        hx, hy = game['H']
        hx, hy = hx + vx, hy + vy
        game['H'] = (hx, hy)
        tx, ty = game['T']
        dx = hx - tx
        dy = hy - ty
        if abs(dx) > 1 or abs(dy) > 1:
            # tail needs to move
            if abs(dx) > 0:
                tx = tx + int(math.copysign(1, dx))
            if abs(dy) > 0:
                ty = ty + int(math.copysign(1, dy))
        tail = (tx, ty)
        game['T'] = tail
        if not tail in tails:
            tails[tail] = True
    return (game, tails)
    

game = { 'H': (0, 0), 'T': (0, 0)}
vecs = { 'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0) }
tails = {(0,0): True}

stdin = sys.stdin.read().splitlines()

for move in parse_lines(stdin):
    # print(f"move: {move}")
    game, tails = apply_move(game, move, vecs, tails)
    # print(f"game: {game}")
    # print(f"tails: {tails}")

print(len(tails))
