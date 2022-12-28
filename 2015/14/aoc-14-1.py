#!/usr/bin/env /usr/bin/python3

import sys
import re
from dataclasses import dataclass

parse_re = re.compile("^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$")

@dataclass
class Reindeer:
    name: str
    speed: int
    fly_duration: int
    rest_duration: int
    def distance_after(self, t):
        cycle_time = self.fly_duration + self.rest_duration
        whole = t // cycle_time
        part = t % cycle_time
        distance = whole * self.speed * self.fly_duration
        part = min(part, self.fly_duration)
        distance += part * self.speed
        return distance

def parse_line(line):
    m = parse_re.match(line)
    return Reindeer(
        name = m.group(1),
        speed = int(m.group(2)),
        fly_duration = int(m.group(3)),
        rest_duration = int(m.group(4))
    )

reindeer = map(parse_line, sys.stdin)

print(max(map(lambda r: r.distance_after(2503), reindeer)))
