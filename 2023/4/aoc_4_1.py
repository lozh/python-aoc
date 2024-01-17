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
    hits = sum(1 for x in game.win if x in game.mine)
    if hits > 0:
        return 2 ** (hits - 1)
    else:
        return 0

stdin = map(str.rstrip, sys.stdin)
games = map(parse_game, stdin)
print(sum(map(score_game, games)))
