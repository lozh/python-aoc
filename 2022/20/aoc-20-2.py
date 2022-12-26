#!/usr/bin/env /usr/bin/python3

import sys
from itertools import cycle

def mix(l):
    id_list = list(enumerate(l))
    out = id_list.copy()
    length = len(id_list)
    n = length - 1
    for _ in range(10):
        for i, x in id_list:
            # print([x for _, x in out])
            if x == 0:
                continue
            j = out.index((i, x))
            k = ((j + x - 1) % n) + 1
            # move item from position j to position k
            del out[j]
            out.insert(k, (i, x))

    # print([x for _, x in out])
    return [x for _, x in out]

# treat file as a list of integers
def read_file(lines):
    for line in map(str.rstrip, lines):
        yield int(line)

file = list(read_file(sys.stdin))

key = 811589153
file = list(map(lambda x: x * key, file))

mixed = mix(file)
l = len(mixed)
i = mixed.index(0)
x = mixed[(i + 1000) % l]
y = mixed[(i + 2000) % l]
z = mixed[(i + 3000) % l]

print(x + y + z)


