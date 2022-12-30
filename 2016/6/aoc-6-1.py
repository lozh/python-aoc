#!/usr/bin/env /usr/bin/python3

import sys
from collections import Counter

def update_counters(counters, word):
    for i in range(len(word)):
        if i == len(counters):
            counters.append(Counter())
        counters[i][word[i]] += 1
    return counters

counters = []

for word in map(str.rstrip, sys.stdin):
    counters = update_counters(counters, word)

print("".join(c.most_common(1)[0][0] for c in counters))
