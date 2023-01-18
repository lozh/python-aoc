#!/usr/bin/env /usr/bin/python3

import sys
from collections import namedtuple
from dataclasses import dataclass

@dataclass
class State:
    registers: dict
    instructions: list
    pc: int

def inc(state, r):
    state.registers[r] += 1
    state.pc += 1
    return state

def dec(state, r):
    state.registers[r] -= 1
    state.pc += 1
    return state

def cpy(state, s, d):
    if d in state.registers:
        if s in state.registers:
            state.registers[d] = state.registers[s]
        else:
            state.registers[d] = int(s)
    state.pc += 1
    return state

def jnz(state, r, o):
    if r in state.registers:
        v = state.registers[r]
    else:
        v = int(r)
    if o in state.registers:
        o = state.registers[o]
    else:
        o = int(o)
    if v == 0:
        state.pc += 1
    else:
        state.pc += o
    return state

toggles = {
    "inc": "dec",
    "dec": "inc",
    "tgl": "inc",
    "jnz": "cpy",
    "cpy": "jnz"
}

def tgl(state, r):
    v = state.pc + state.registers[r]
    if v >=0 and v < len(state.instructions):
        i = state.instructions[v]
        cmd = i[:3]
        cmd = toggles[cmd]
        state.instructions[v] = cmd + i[3:]
    state.pc += 1
    return state

decodes = {
    "inc": inc,
    "dec": dec,
    "cpy": cpy,
    "jnz": jnz,
    "tgl": tgl
}

def decode(i):
    if i[:3] in decodes:
        return decodes[i[:3]]
    raise Exception(f"Unknown instruction {i}")

def apply(state, i):
    f = decode(i)
    args = i[4:].split(" ")
    state = f(state, *args)
    return state

def run(state):
    while state.pc < len(state.instructions):
        i = state.instructions[state.pc]
        state = apply(state, i)
    return state
    
state = State(
    registers = {"a": 7, "b": 0, "c": 0, "d": 0},
    instructions = list(map(str.rstrip, sys.stdin)),
    pc = 0
)

state = run(state)

print(state.registers["a"])
