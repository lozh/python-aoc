#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Dir:
    x: int
    y: int

@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def move(self, d: Dir):
        return Pos(self.x + d.x, self.y + d.y)

@dataclass(frozen=True)
class Trench:
    direction: Dir
    distance: int

@dataclass
class Dig:
    pos: Pos
    dug: set[Pos]
    start_dir: Dir
    cur_dir: Dir

    def __init__(self):
        self.pos = Pos(0, 0)
        self.dug = {self.pos: 'S'}
        self.start_dir = None
        self.cur_dir = None
    
    def dig(self, trench: Trench):
        if self.start_dir:
            self.dug[self.pos] = turn_char[self.cur_dir, trench.direction]
        else:
            self.start_dir = trench.direction
        self.cur_dir = trench.direction
        for _ in range(trench.distance):
            self.pos = self.pos.move(trench.direction)
            if self.pos in self.dug:
                # by inspection, this only happens as the loop is closed
                self.dug[self.pos] = turn_char[self.cur_dir, self.start_dir]
            else:
                self.dug[self.pos] = dir_char[trench.direction]
                
    def fill_count(self):
        count = 0
        xn = min(p.x for p in self.dug)
        yn = min(p.y for p in self.dug)
        xx = max(p.x for p in self.dug)
        yx = max(p.y for p in self.dug)
        print(yn, yx)
        for y in range(yn, yx + 1):
            print(y)
            inside = False
            corner = None
            for x in range(xn, xx + 1):
                p = Pos(x, y)
                cell = self.dug.get(p, ' ')
                #print(cell)
                match cell:
                    case ' ':
                        count += 1 if inside else 0
                    case '|':
                        count += 1
                        inside = not inside
                    case '-':
                        count += 1
                    case 'F' | 'L':
                        count += 1
                        corner = cell
                    case '7':
                        count += 1
                        if corner == 'L':
                            inside = not inside
                    case 'J':
                        count += 1
                        if corner == 'F':
                            inside = not inside
        return count
                            
                        
                
        
dir_map = {
    'U': Dir(0, -1),
    'R': Dir(1, 0),
    'D': Dir(0, 1),
    'L': Dir(-1, 0),
}

dir_char = {
    Dir(0, -1): '|',
    Dir(1, 0): '-',
    Dir(0, 1): '|',
    Dir(-1, 0): '-',

}

turn_char = {
    (Dir(0, -1), Dir(1, 0)): 'F',
    (Dir(0, -1), Dir(-1, 0)): '7',
    (Dir(-1, 0), Dir(0, -1)): 'L',
    (Dir(-1, 0), Dir(0, 1)): 'F',
    (Dir(0, 1), Dir(-1, 0)): 'J',
    (Dir(0, 1), Dir(1, 0)): 'L',
    (Dir(1, 0), Dir(0, -1)): 'J',
    (Dir(1, 0), Dir(0, 1)): '7'
}

def parse(line: str) -> Trench:
    m = re.match(r"([RDLU]) (\d+)", line)
    return Trench(dir_map[m[1]], int(m[2]))


lines = map(str.rstrip, sys.stdin)
dig = Dig()

for trench in map(parse, lines):
    dig.dig(trench)

print(dig.fill_count())

# This outputs the length of the perimeter
#print(len(dig.dug))

# This outputs a map that aoc_10_2.py can read and return the filled area
#for y in range(yn, yx + 1):
#    print("".join(dig.dug.get(Pos(x, y), '.') for x in range(xn, xx + 1)))


        
