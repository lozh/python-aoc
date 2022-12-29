#!/usr/bin/env /usr/bin/python3

import sys
from itertools import repeat

min_qe = (999, 99999999)


def parts(buckets, target, left):
    try:
        global min_qe
        if buckets[0][1] < min_qe[0] or (buckets[0][1] == min_qe[0] and buckets[0][2] <= min_qe[1]):
            if not left:
                min_qe = (buckets[0][1], buckets[0][2])
                yield buckets[0]
            else:
                if buckets[0][0] == target:
                    n, *left = left
                    # if bucket 0 already full, we only need one solution for the other buckets
                    for i, (t, l, q) in enumerate(buckets):
                        if t + n <= target:
                            nb = [x for x in buckets]
                            nb[i] = (t + n, l + 1, q * n)
                            _ = next(parts(nb, target, left))
                            yield buckets[0]
                else:
                    n, *left = left
                    for i, (t, l, q) in enumerate(buckets):
                        if t + n <= target:
                            nb = [x for x in buckets]
                            nb[i] = (t + n, l + 1, q * n)
                            yield from parts(nb, target, left)
    except GeneratorExit:
        pass
    
def partitions(nums, count):
    target = sum(nums) // count
    if sum(nums) % count != 0:
        raise Exception("no solutions")
    buckets = list(repeat((0, 0, 1), count))
    yield from parts(buckets, target, nums)
    

nums = list(map(int, map(str.rstrip, sys.stdin)))
nums = list(sorted(nums, reverse = True))

for p in partitions(nums, 3):
    print(p)
