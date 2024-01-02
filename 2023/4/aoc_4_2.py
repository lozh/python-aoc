#!/usr/bin/env python3

import sys
import re
import string
from dataclasses import dataclass


@dataclass
class Game:
    win: list[int]
    mine: list[int]

    def __str__(self) -> str:
        return f"{self.win} | {self.mine}"

game_re = re.compile("Card\s+\d+: ([^|]+)\| (.*)")

def parse_game(line):
    m = game_re.match(line)
    win = m[1].split()
    mine = m[2].split()
    return Game(win, mine)

def score_game(game):
    return sum(1 for x in game.win if x in game.mine)

stdin = map(str.rstrip, sys.stdin)
games = map(parse_game, stdin)

copies = []
total = 0

for game in games:
    score = score_game(game)
    if copies:
        n = copies.pop(0) + 1
    else:
        n = 1
    total += n
    for i in range(score):
        if i < len(copies):
            copies[i] += n
        else:
            copies.append(n)

print(total)
