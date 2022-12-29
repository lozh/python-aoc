#!/usr/bin/env /usr/bin/python3

import sys

def hlf(state, r):
    state["pc"] += 1
    state[r] //= 2
    return state

def tpl(state, r):
    state["pc"] += 1
    state[r] *= 3
    return state

def inc(state, r):
    state["pc"] += 1
    state[r] += 1
    return state

def jmp(state, o):
    state["pc"] += int(o)
    return state

def jie(state, r, o):
    if state[r] % 2 == 0:
        state["pc"] += int(o)
    else:
        state["pc"] += 1
    return state

def jio(state, r, o):
    if state[r] == 1:
        state["pc"] += int(o)
    else:
        state["pc"] += 1
    return state

decode = {
    "hlf": hlf,
    "tpl": tpl,
    "inc": inc,
    "jmp": jmp,
    "jie": jie,
    "jio": jio,
}

initial = {
    "pc": 0,
    "a": 1,
    "b": 0,
}

instructions = list(map(str.rstrip, sys.stdin))

state = initial
while True:
    if state["pc"] < 0 or state["pc"] >= len(instructions):
        break
    i = instructions[state["pc"]]
    f = decode[i[0:3]]
    a = list(map(str.strip, i[4:].split(",")))
    state = f(state, *a)

print(state["b"])
