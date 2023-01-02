#!/usr/bin/env /usr/bin/python3

import sys

def dragon(a):
    b = "".join(reversed(['1' if c == '0' else '0' for c in  a]))
    return a + '0' + b

def find_image(seed, target_len):
    while len(seed) < target_len:
        seed = dragon(seed)
    return seed[:target_len]

def checksum(image):
    if len(image) % 2 == 1:
        return image
    else:
        ret = []
        for i in range(len(image)//2):
            if image[i * 2] == image[i * 2 + 1]:
                ret.append("1")
            else:
                ret.append("0")
        return checksum("".join(ret))

seed = sys.stdin.readline().strip()
target_len = 35651584
image = find_image(seed, target_len)
print(checksum(image))

