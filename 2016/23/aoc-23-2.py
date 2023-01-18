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
# inc r1
# dec r2
# jnz r2 -2
# dec r3
# jnz r3 -5
# is equivalent to r1 = r1 + r2 * r3
def peephole_multiply(state):
    if state.pc + 5 > len(state.instructions):
        return None
    i0 = state.instructions[state.pc]
    if i0[:3] != "inc":
        return None
    r1 = i0[4:]
    i1 = state.instructions[state.pc + 1]
    if i1[:3] != "dec":
        return None
    r2 = i1[4:]
    if r1 == r2:
        print(i0, r1, i1, r2)
        return None
    i2 = state.instructions[state.pc + 2]
    if i2[:3] != "jnz":
        return None
    a2 = i2[4:].split(" ")
    if a2[0] != r2:
        return None
    if a2[1] != "-2":
        return None
    i3 = state.instructions[state.pc + 3]
    if i3[:3] != "dec":
        return None
    r3 = i3[4:]
    if r3 == r1 or r3 == r2:
        return None
    i4 = state.instructions[state.pc + 4]
    if i4[:3] != "jnz":
        return None
    a4 = i4[4:].split(" ")
    if a4[0] != r3:
        return None
    if a4[1] != "-5":
        return None
    state.registers[r1] += state.registers[r2] * state.registers[r3]
    state.pc += 5
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
