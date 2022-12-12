#!/usr/bin/env /usr/bin/python3

import sys
import re
import functools
from functools import reduce
import gmpy2
from gmpy2 import mpz, lcm

monkeys = []

monkey_re = re.compile("^Monkey (\d+):$")
items_re = re.compile("^  Starting items: (.*)$")
op_re = re.compile("^  Operation: new = (.*)$")
test_re = re.compile("^  Test: divisible by (.*)$")
true_re = re.compile("^    If true: throw to monkey (\d+)$")
false_re = re.compile("^    If false: throw to monkey (\d+)$")

def parse_monkey(lines):
    m = monkey_re.match(lines.__next__())
    monkey_no = int(m.group(1))
    m = items_re.match(lines.__next__())
    items = list(map(mpz, map(lambda s: s.strip(), m.group(1).split(","))))
    m = op_re.match(lines.__next__())
    op = m.group(1)
    m = test_re.match(lines.__next__())
    div = int(m.group(1))
    m = true_re.match(lines.__next__())
    true_to = int(m.group(1))
    m = false_re.match(lines.__next__())
    false_to = int(m.group(1))
    monkey = {
        "monkey_no": monkey_no,
        "items": items,
        "op": compile(op, op, "eval"),
        "div": div,
        "throw_func": lambda x: true_to if x % div == 0 else false_to,
        "inspect_count": 0,
    }

    return stdin, monkey

def process_round(monkeys, lcm):
    for monkey in monkeys:
        for old in monkey["items"]:
            monkey["inspect_count"] += 1
            # I checked the input is sensible by eye
            old = eval(monkey["op"]) % lcm
            to = monkey["throw_func"](old)
            monkeys[to]["items"].append(old)
        # assume monkey doesn't throw to self
        monkey["items"] = []
    return monkeys
        

stdin = sys.stdin

while True:
    stdin, monkey = parse_monkey(stdin)
    monkeys.append(monkey)
    try:
        stdin.__next__()
    except:
        break

lcm = reduce(lcm, (m["div"] for m in monkeys))

for i in range(10000):
    monkeys = process_round(monkeys, lcm)

inspect_counts = (m["inspect_count"] for m in monkeys)
top_2 = sorted(inspect_counts, reverse = True)[0:2]
print(top_2[0] * top_2[1])
