#!/usr/bin/env python3

import sys
import re

from dataclasses import dataclass

@dataclass
class MapEntry:
    src: int
    dest: int
    length: int

@dataclass
class Map:
    src: str
    dest: str
    entries: list[MapEntry]

    def my_map(self, key) -> int:
        for entry in self.entries:
            if key >= entry.src and key < (entry.src + entry.length):
                return entry.dest + key - entry.src
        return key

@dataclass
class Almanac:
    seeds: list[int]
    maps: list[Map]
    def seed_map(self):
        for seed in self.seeds:
            for m in self.maps:
                seed = m.my_map(seed)
            yield seed

def parse(stdin):
    state = 0
    maps = []
    src = ""
    for line in stdin:
        match state:
            # Seeds
            case 0:
                m = re.match(r"seeds: (.*)", line)
                seeds = list(map(int, m[1].split()))
                state = 1
            # Expect map entry or blank
            case 1:
                if line == "":
                    if src != "":
                        maps.append(Map(src, dest, entries))
                    state = 2
                else:
                    p = line.split()
                    entries.append(MapEntry(int(p[1]), int(p[0]), int(p[2])))
            # Expect map header
            case 2:
                m = re.match(r"([^-]+)-to-([^-]+) map:", line)
                src = m[1]
                dest = m[2]
                entries = []
                state = 1

    maps.append(Map(src, dest, entries))
    return Almanac(seeds, maps)
                

a = parse(map(str.rstrip, sys.stdin))
# print(a)
sm = a.seed_map()
print(min(sm))
