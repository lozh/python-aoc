#!/usr/bin/env /usr/bin/python3

import sys

# easier to deal with pos as [(x, y)] rather than [x][y]
# as not performance critical
def lists_to_dict(height_map):
    for row, line in enumerate(height_map):
        for col, char in enumerate(line):
            yield row, col, char

# possible neighbours of pos
def neighbours(pos, rows, cols):
    x, y = pos
    if x > 0: yield x - 1, y
    if x < rows - 1: yield x + 1, y
    if y > 0: yield x, y - 1
    if y < cols - 1: yield x, y + 1

# neighbours of pos that we are allowed to travel to
def permissible_neighbours(height_map, pos, rows, cols):
    h = height_map[pos]
    for npos in neighbours(pos, rows, cols):
        n = height_map[npos]
        # height check
        if ord(n) - 1 <= ord(h):
            yield npos

def find_char(char, height_map):
    pos = [pos for pos, value in height_map.items() if value == char]
    return pos[0]

# count minimum steps to get from start to end
# we have an expanding frontier of places we can reach
# until we hit the end
def count_steps(height_map, start, end, rows, cols):
    steps = 0
    visited = {start: steps}
    starts = [start]

    while True:
        steps += 1
        next_starts = []
        for start in starts:
            for n in permissible_neighbours(height_map, start, rows, cols):
                if n == end:
                    return steps
                if not n in visited:
                    visited[n] = steps
                    next_starts.append(n)
        if next_starts == []:
            raise "no solution"
        starts = next_starts

# read input as a list of lists of chars
height_map = list(map(lambda line: [*(line.rstrip())], sys.stdin))
rows = len(height_map)
cols = len(height_map[0])

# convert height_map to dict of (x, y) -> height
height_map = {(row, col):char for row, col, char in lists_to_dict(height_map)}

start  = find_char('S', height_map)
end = find_char('E', height_map)

height_map[start] = 'a'
height_map[end] = 'z'

print(count_steps(height_map, start, end, rows, cols))
