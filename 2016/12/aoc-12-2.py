#!/usr/bin/env /usr/bin/python3

import sys
from collections import namedtuple


def inc(state, r):
    state[r] += 1
    state["pc"] += 1
    return state

def dec(state, r):
    state[r] -= 1
    state["pc"] += 1
    return state

def cpy(state, s, d):
    if s in state:
        state[d] = state[s]
    else:
        state[d] = int(s)
    state["pc"] += 1
    return state

def jnz(state, r, o):
    if r in state:
        v = state[r]
    else:
        v = int(r)
    if v == 0:
        state["pc"] += 1
    else:
        state["pc"] += int(o)
    return state

def decode(i):
    if i[:3] == "inc":
        return inc
    if i[:3] == "dec":
        return dec
    if i[:3] == "cpy":
        return cpy
    if i[:3] == "jnz":
        return jnz
    raise Exception(f"Unknown instruction {i}")

def apply(state, i):
    f = decode(i)
    args = i[4:].split(" ")
    state = f(state, *args)
    return state

def run(state, instructions):
    while state["pc"] < len(instructions):
        i = instructions[state["pc"]]
        state = apply(state, i)
    return state
    
state = {}
for x in ["a", "b", "c", "d", "pc"]:
    state[x] = 0
state["c"] = 1
state = run(state, list(map(str.rstrip, sys.stdin)))

print(state["a"])
