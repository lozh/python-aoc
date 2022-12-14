#!/usr/bin/env /usr/bin/python3

import sys

def find_chunk(line, n):
    chunk_count = len(line)
    for i, s in [(i, line[i:i + n]) for i in range(chunk_count)]:
        if len(set(s)) == n:
            return i + n

line = sys.stdin.readline()

print(find_chunk(line, 14))
