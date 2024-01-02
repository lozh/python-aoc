#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from collections import Counter
from enum import IntEnum
from operator import attrgetter
from functools import cmp_to_key

cards = list("AKQJT98765432")

class HandType(IntEnum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7

def cards_to_type(cards: str) -> HandType:
    counts = list(Counter(cards).values())
    counts.sort(reverse = True)
    if counts[0] == 5:
        return HandType.FIVE_OF_A_KIND
    if counts[0] == 4:
        return HandType.FOUR_OF_A_KIND
    if counts[0] == 3 and counts[1] == 2:
        return HandType.FULL_HOUSE
    if counts[0] == 3:
        return HandType.THREE_OF_A_KIND
    if counts[0] == 2 and counts[1] == 2:
        return HandType.TWO_PAIR
    if counts[0] == 2:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD
    
@dataclass
class Game:
    cards: str
    hand_type: HandType
    bid: int

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        self.hand_type = cards_to_type(cards)

    def cmp(self, other):
        if self.hand_type < other.hand_type:
            return -1
        if self.hand_type > other.hand_type:
            return 1
        for (s1, o1) in zip(self.cards, other.cards):
            if cards.index(s1) < cards.index(o1):
                return -1
            if cards.index(s1) > cards.index(o1):
                return 1
        return 0

def parse(line) -> Game:
    (cards, bid) = line.split()
    return Game(cards, int(bid))

games = map(lambda x: parse(str.rstrip(x)), sys.stdin)

g = sorted(games, key = cmp_to_key(Game.cmp), reverse = True)
scores = map(lambda xg: xg[0] * xg[1].bid, enumerate(g, start = 1))
print(sum(list(scores)))
