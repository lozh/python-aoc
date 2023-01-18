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

# look for a multiply sequence
# cpy r4 r2
# inc r1
# dec r2
# jnz r2 -2
# dec r3
# jnz r3 -5
# is equivalent to:
# r1 = r1 + r3 * r4
# r2 = 0
# r3 = 0
def peephole_multiply(state):
    pc = state.pc
    if pc + 6 > len(state.instructions):
        return None
    i = state.instructions[pc]
    if i[:3] != "cpy":
        return None
    r4, r2 = i[4:].split(" ")
    if r4 not in state.registers:
        return None
    if r2 not in state.registers:
        return None
    pc += 1
    i = state.instructions[pc]
    if i[:3] != "inc":
        return None
    r1 = i[4:]
    if r1 == r4 or r1 == r2:
        return None
    pc += 1
    i = state.instructions[pc]
    if i[:3] != "dec":
        return None
    if i[4:] != r2:
        return None
    pc += 1
    i = state.instructions[pc]
    if i[:3] != "jnz":
        return None
    a2 = i[4:].split(" ")
    if a2[0] != r2:
        return None
    if a2[1] != "-2":
        return None
    pc += 1
    i = state.instructions[pc]
    if i[:3] != "dec":
        return None
    r3 = i[4:]
    if r1 == r3 or r2 == r3 or r4 == r3:
        return None
    pc += 1
    i = state.instructions[pc]
    if i[:3] != "jnz":
        return None
    a4 = i[4:].split(" ")
    if a4[0] != r3:
        return None
    if a4[1] != "-5":
        return None
    state.registers[r1] += state.registers[r3] * state.registers[r4]
    state.registers[r2] = 0
    state.registers[r3] = 0
    state.pc += 6
    return state


def process(state):
    if s := peephole_multiply(state):
        return s

    i = state.instructions[state.pc]
    f = decode(i)
    args = i[4:].split(" ")
    state = f(state, *args)
    return state

def run(state):
    while state.pc < len(state.instructions):
        state = process(state)
    return state
    
state = State(
    registers = {"a": 12, "b": 0, "c": 0, "d": 0},
    instructions = list(map(str.rstrip, sys.stdin)),
    pc = 0
)

state = run(state)

print(state.registers["a"])
