#!/usr/bin/env python3
import sys
import re

from dataclasses import dataclass

@dataclass
class MapEntry:
    src: int
    dest: int
    length: int

    def as_range(self):
        return Range(self.src, self.length)

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

    # take an input range
    # yield output ranges
    def map_range(self, range):
        ranges = [range]
        for entry in self.entries:
            new_ranges = []
            for r in ranges:
                # does the input range overlap the key range at all?
                i = r.intersect(entry.as_range())
                if (i):
                    yield Range(i.start + entry.dest - entry.src, i.length)
                    if r.start < i.start:
                        new_ranges.append(Range(r.start, i.start - r.start))
                    if r.end() > i.end():
                        new_ranges.append(Range(i.end(), r.end() - i.end()))
                else:
                    new_ranges.append(r)
            ranges = new_ranges
        # Things that weren't hit by any of the ranges in the map
        yield from ranges

@dataclass
class Range:
    start: int
    length: int

    def end(self):
        return self.start + self.length

    def intersect(self, range):
        istart = max(self.start, range.start)
        iend = min(self.end(), range.end())
        if istart >= iend:
            return None
        else:
            return Range(istart, iend - istart)

@dataclass
class Almanac:
    seeds: list[Range]
    maps: list[Map]
    def seed_map(self):
        ranges = self.seeds
        for m in self.maps:
            new_ranges = []
            for r in ranges:
                new_ranges.extend(m.map_range(r))
            ranges = new_ranges
        return ranges

def parse_seeds(pairs):
    seeds = []

    while pairs:
        start = pairs[0]
        length = pairs[1]
        pairs = pairs[2:]
        seeds.append(Range(start, length))
    return seeds

def parse(stdin):
    state = 0
    maps = []
    src = ""
    for line in stdin:
        match state:
            # Seeds
            case 0:
                m = re.match(r"seeds: (.*)", line)
                pairs = list(map(int, m[1].split()))
                seeds = parse_seeds(pairs)
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
sm = a.seed_map()
ans = min(map(lambda x: x.start, sm))
print(ans)
