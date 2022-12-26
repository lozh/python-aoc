#!/usr/bin/env /usr/bin/python3

import sys
import re

line_re = re.compile("^([a-z]+): (.*)$")
num_re = re.compile("^(\d+)$")
op_re = re.compile("^([a-z]+) (\+|\-|\*|\/) ([a-z]+)$")

ops = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x // y
}

def my_eval(expr, expressions):
    x = expressions[expr]
    m = num_re.match(x)
    if m:
        return int(m.group(1))

    m = op_re.match(x)
    if m:
        op = m.group(2)
        op = ops[op]
        arg1 = m.group(1)
        arg2 = m.group(3)
        return op(my_eval(arg1, expressions), my_eval(arg2, expressions))

def parse_line(line):
    m = line_re.match(line)
    return str(m.group(1)), m.group(2)

# print(list(map(parse_line, sys.stdin)))
expressions = { k:v for (k, v) in map(parse_line, sys.stdin) }

print(my_eval("root", expressions))

