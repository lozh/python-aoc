#!/usr/bin/env /usr/bin/python3

import sys
import re
from dataclasses import dataclass

parse_re = re.compile("^(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)$")

@dataclass(frozen=True)
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

max_t = 100

def parse_ingredient(line):
    m = parse_re.match(line)
    return Ingredient(
        name = m.group(1),
        capacity = int(m.group(2)),
        durability = int(m.group(3)),
        flavor = int(m.group(4)),
        texture = int(m.group(5)),
        calories = int(m.group(6))
    )

def score(ingredient_counts):
    capacity = sum(map(lambda ic: ic[0].capacity * ic[1], ingredient_counts))
    if capacity < 0: capacity = 0
    durability = sum(map(lambda ic: ic[0].durability * ic[1], ingredient_counts))
    if durability < 0: durability = 0
    flavor = sum(map(lambda ic: ic[0].flavor * ic[1], ingredient_counts))
    if flavor < 0: flavor = 0
    texture = sum(map(lambda ic:ic[0].texture * ic[1], ingredient_counts))
    if texture < 0: texture = 0
    calories = sum(map(lambda ic:ic[0].calories * ic[1], ingredient_counts))
    return capacity * durability * flavor * texture, calories

def recipies(ingredients, max_t):
    if len(ingredients) == 1:
        yield [(ingredients[0], max_t)]
        return

    for t in range(max_t):
        i = ingredients.pop()
        for r in recipies(ingredients, max_t - t):
            yield [(i, t)] + r
        ingredients.append(i)

ingredients = list(map(parse_ingredient, sys.stdin))
print(max(score for score, cal in map(score, recipies(ingredients, max_t)) if cal == 500))

