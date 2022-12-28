#!/usr/bin/env /usr/bin/python3

import sys
from itertools import repeat

def is_valid(s):
    # Does it contain three consecutive letters?
    ret = False
    for i in range(len(s) - 2):
        if ord(s[i]) == ord(s[i + 1]) - 1 and ord(s[i + 1]) == ord(s[i + 2]) - 1:
            ret = True
            break

    if not ret:
        return ret

    # Does it contain i, o or l?
    if s.find('i') > -1 or s.find('o') > -1 or s.find('l') > -1:
        return False

    # Does it contain two different pairs?
    pairs = set()
    for i in range(len(s) - 1):
        if s[i] == s[i + 1] and s[i] not in pairs:
            pairs.add(s[i])
            if len(pairs) == 2:
                return True

    return False

def next_trial(s):
    # If s contains i, o or l then we can skip a bunch of trials
    p = [s.find('i'), s.find('o'), s.find('l')]
    p = [i for i in p if i != -1]
    if p:
        offset = min(p)
        return s[0:offset] + chr(ord(s[offset]) + 1) + "".join(repeat('a', len(s) - offset - 1))

    chars = [c for c in s]
    for i in range(len(s) - 1, -1, -1):
        if chars[i] != 'z':
            chars[i] = chr(ord(chars[i]) + 1)
            break
        else:
            chars[i] = 'a'

    return "".join(chars)
    
i = str.rstrip(next(sys.stdin))
i = next_trial(i)

while not is_valid(i):
    i = next_trial(i)

i = next_trial(i)

while not is_valid(i):
    i = next_trial(i)
    
print(i)
    
