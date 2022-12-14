#!/usr/bin/env /usr/bin/python3

import sys
import re

signal_re = re.compile("^([a-z]+|\d+) -> ([a-z]+)$")
binary_re = re.compile("^([a-z]+|\d+) (AND|OR) ([a-z]+|\d+) -> ([a-z]+)$")
shift_re = re.compile("^([a-z]+|\d+) (RSHIFT|LSHIFT) (\d+) -> ([a-z]+)$")
not_re = re.compile("NOT ([a-z]+|\d+) -> ([a-z]+)$")

wire_re = re.compile("^([a-z]+)$")
val_re = re.compile("^(\d+)$")

mask = 65535

ops = {
    "AND": lambda x: x[0] & x[1],
    "OR": lambda x: x[0] | x[1],
    "NOT": lambda x: ~x[0] & mask,
    "LSHIFT": lambda n: lambda x: (x[0] << n) & mask,
    "RSHIFT": lambda n: lambda x: (x[0] >> n)
}

class Place:
    def __init__(self, value):
        self.value = value

class Wire(Place):
    def __init__(self, value):
        super().__init__(value)

    def apply(self, bindings):
        return bindings[self.value]

    def is_bound(self, bindings):
        return self.value in bindings

class Signal(Place):
    def __init__(self, value):
        super().__init__(value)

    def apply(self, bindings):
        return self.value

    def is_bound(self, bindings):
        return True

def parse_place(place):
    m = wire_re.match(place)
    if m:
        return Wire(m.group(1))

    m = val_re.match(place)
    if m:
        return Signal(int(m.group(1)))

    print("Could not parse place: {place}")
    raise

def parse_instruction(line):
    m = signal_re.match(line)
    if m:
        return {
            "tag": "signal",
            "inputs": [parse_place(m.group(1))],
            "output": m.group(2),
            "op": lambda x: x[0]
        }
    m = binary_re.match(line)
    if m:
        return {
            "tag": m.group(2),
            "inputs": [parse_place(m.group(1)), parse_place(m.group(3))],
            "output": m.group(4),
            "op": ops[m.group(2)]
        }
    m = shift_re.match(line)
    if m:
        return {
            "tag": m.group(2),
            "inputs": [parse_place(m.group(1))],
            "output": m.group(4),
            "op": ops[m.group(2)](int(m.group(3)))
        }
    m = not_re.match(line)
    if m:
        return {
            "tag": "NOT",
            "inputs": [parse_place(m.group(1))],
            "output": m.group(2),
            "op": ops["NOT"]
        }
    print(f"Couldn't parse: {line}")
    raise

def emulate(instructions, bindings):
    instructions = list(instructions)
    while instructions:
        unsolved_instructions = []
        for i in instructions:
            if all(input.is_bound(bindings) for input in i["inputs"]):
                vals = [input.apply(bindings) for input in i["inputs"]]
                op = i["op"]
                if not i["output"] in bindings:
                    bindings[i["output"]] = op(vals)
            else:
                unsolved_instructions.append(i)
        instructions = unsolved_instructions
    return bindings


bindings = {}
instructions = list(map(parse_instruction, sys.stdin))
bindings = emulate(instructions, bindings)
bindings = { 'b': bindings['a'] }
bindings = emulate(instructions, bindings)
print(bindings['a'])
