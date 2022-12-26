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

inverses = {
    '+': lambda result, a1, a2: result - a1 if a2 == None else result - a2,
    '-': lambda result, a1, a2: a1 - result if a2 == None else result + a2,
    '*': lambda result, a1, a2: result // a1 if a2 == None else result // a2,
    '/': lambda result, a1, a2: a1 // result if a2 == None else result * a2
}

def my_eval(expr, humn, expressions):
    # print(f"my_eval({expr}, {humn})")
    if expr == humn:
        return None
    x = expressions[expr]
    m = num_re.match(x)
    if m:
        return int(m.group(1))

    m = op_re.match(x)
    if m:
        op = m.group(2)
        op = ops[op]
        arg1 = my_eval(m.group(1), humn, expressions)
        arg2 = my_eval(m.group(3), humn, expressions)
        if arg1 == None or arg2 == None:
            return None
        else:
            return op(arg1, arg2)

def solve(expr, humn, val, expressions):
    # print(f"solve({expr}, {humn}, {val})")
    root = expressions[expr]
    m = op_re.match(root)
    if m:
        op = m.group(2)
        op = inverses[op]
        arg1 = m.group(1)
        arg2 = m.group(3)
        if arg1 == humn:
            right = my_eval(arg2, humn, expressions)
            return op(val, None, right)
        if arg2 == humn:
            left = my_eval(arg1, humn, expressions)
            return op(val, left, None)
        left = my_eval(arg1, humn, expressions)
        right = my_eval(arg2, humn, expressions)
        if left == None:
            if val == None:
                return solve(arg1, humn, right, expressions)
            else:
                return solve(arg1, humn, op(val, left, right), expressions)
        elif right == None:
            if val == None:
                return solve(arg2, humn, left, expressions)
            else:
                return solve(arg2, humn, op(val, left, right), expressions)
        else:
            print("Oops")
            raise
    else:
        print("Oops")

def parse_line(line):
    m = line_re.match(line)
    return str(m.group(1)), m.group(2)

# print(list(map(parse_line, sys.stdin)))
expressions = { k:v for (k, v) in map(parse_line, sys.stdin) }

print(solve("root", "humn", None, expressions))

