#!/usr/bin/env /usr/bin/python3

import sys

def encode(s):
    ret = ""
    i = 0
    while i < len(s):
        c = s[i]
        j = i + 1
        while j < len(s):
            if s[j] == c:
                j += 1
            else:
                break
        n = j - i
        i += n
        ret = ret + str(n) + c
    return ret

line = sys.stdin.readline().rstrip()

for i in range(40):
    line = encode(line)

print(len(line))
