#!/usr/bin/env /usr/bin/python3

from dataclasses import dataclass
from itertools import product

@dataclass
class Item:
    name: str
    cost: int
    armor: int = 0
    damage: int = 0

@dataclass
class Actor:
    armor: int
    damage: int
    hp: int

weapons = [
    Item(name = "Dagger", cost = 8, damage = 4),
    Item(name = "Shortsword", cost = 10, damage = 5),
    Item(name = "Warhammer", cost = 25, damage = 6),
    Item(name = "Longsword", cost = 40, damage = 7),
    Item(name = "Greataxe", cost = 74, damage = 8)
]

armors = [
    None,
    Item(name = "Leather", cost = 13, armor = 1),
    Item(name = "Chainmail", cost = 31, armor = 2),
    Item(name = "Splintmail", cost = 53, armor = 3),
    Item(name = "Bandedmail", cost = 75, armor = 4),
    Item(name = "Platemail", cost = 102, armor = 5)
]

rings = [
    None,
    Item(name = "Damage +1", cost = 25, damage = 1),
    Item(name = "Damage +2", cost = 50, damage = 2),
    Item(name = "Damage +3", cost = 100, damage = 3),
    Item(name = "Defense +1", cost = 20, armor = 1),
    Item(name = "Defense +2", cost = 40, armor = 2),
    Item(name = "Defense +3", cost = 80, armor = 3)
]

# how many rounds would defender survive against attacker
def survive_rounds(attacker, defender):
    damage = attacker.damage - defender.armor
    if damage < 1: damage = 1
    rounds = defender.hp // damage
    if rounds * damage < defender.hp: rounds += 1
    return rounds

def win(me, boss):
    me_rounds = survive_rounds(boss, me)
    boss_rounds = survive_rounds(me, boss)
    return me_rounds >= boss_rounds

def item_selections():
    yield from (filter(None, [w, a, r1, r2]) for w, a, r1, r2 in product(weapons, armors, rings, rings) if r1 == None or r2 == None or r1 != r2)

def character(hp, items):
    armor = 0
    damage = 0
    cost = 0
    for i in items:
        armor += i.armor
        damage += i.damage
        cost += i.cost
    return Actor(hp = hp, armor = armor, damage = damage), cost

boss = Actor(armor = 2, damage = 8, hp = 100)

print(max(c for me, c in map(lambda i: character(100, i), item_selections()) if not win(me, boss)))


