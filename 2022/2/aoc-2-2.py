#!/usr/bin/env /usr/bin/python3

import sys

lookup = {
    ('A', 'X'): 3,
    ('A', 'Y'): 4,
    ('A', 'Z'): 8,
    ('B', 'X'): 1,
    ('B', 'Y'): 5,
    ('B', 'Z'): 9,
    ('C', 'X'): 2,
    ('C', 'Y'): 6,
    ('C', 'Z'): 7    
}

def tuples_to_scores(tuples, lookup):
    return map(lookup.get, tuples)

def input_to_tuples(lines):
    return map(line_to_tuple, lines)

def line_to_tuple(line):
    return (line[0], line[2])

stdin = map(str.rstrip, sys.stdin)
tuples = input_to_tuples(stdin)
scores = tuples_to_scores(tuples, lookup)

print(sum(scores))


