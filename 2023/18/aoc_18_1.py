#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Dir:
    x: int
    y: int

    def reverse(self):
        return Dir(-self.x, -self.y)

@dataclass(frozen=True)
class Move:
    direction: Dir
    distance: int

@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def move(self, m: Move):
        return Pos(self.x + m.direction.x * m.distance, self.y + m.direction.y * m.distance)

@dataclass(frozen=True)
class Trench:
    pos: Pos
    direction: Dir
    distance: int
    end: Pos

    # Normalise to be either south or east
    def __init__(self, pos: Pos, move: Move):
        # object.__setattr__ so we can use frozen=True
        object.__setattr__(self, 'distance', move.distance)
        direction = move.direction
        if direction == Dir(0, -1) or direction == Dir(-1, 0):
            pos = pos.move(move)
            direction = direction.reverse()
            move = Move(direction, move.distance)
        end = pos.move(move)
        object.__setattr__(self, 'pos',  pos)
        object.__setattr__(self, 'direction',  direction)
        object.__setattr__(self, 'end', end)
                
    def is_vert(self):
        return self.direction.x == 0
    
    def yintersects(self, y):
        if self.is_vert():
            return self.pos.y <= y and self.pos.y + self.distance > y
        else:
            return self.pos.y == y

@dataclass
class Dig:
    pos: Pos
    corners: set[Pos]
    trenches: list[Trench]
    start_dir: Dir
    cur_dir: Dir

    def __init__(self):
        self.pos = Pos(0, 0)
        self.corners = {self.pos: 'S'}
        self.trenches = []
        self.start_dir = None
        self.cur_dir = None
    
    def dig(self, move: Move):
        if self.start_dir:
            self.corners[self.pos] = turn_char[self.cur_dir, move.direction]
        else:
            self.start_dir = move.direction
        self.cur_dir = move.direction
        self.trenches.append(Trench(self.pos, move))
        self.pos = self.pos.move(move)
        if self.pos in self.corners:
            # by inspection, this only happens as the loop is closed
            self.corners[self.pos] = turn_char[self.cur_dir, self.start_dir]

    # figure out how many cells are on or inside the boundary for line y
    # given trenches that intersect that line
    # As we scan a line, we start outside the lava and every time we cross
    # an edge we flip from outside to inside or back again
    # For horizontal lines, if the ends curve the same way it doesn't
    # flip whether or not you are inside i.e:
    # ┌──────┐ or └──────┘
    # a horizontal line where the ends curve opposite ways does flip i.e:
    # ┌──────┘ or └──────┐
    # You still need to count the line as part of the boundary either way.
    def line_count(self, y, trenches):
        inside = False
        last_pos = None
        count = 0
        for t in sorted(trenches, key = lambda t: t.pos.x):
            if t.is_vert():
                # process corners as part of the horizontal
                if y == t.pos.y or y == t.end.y:
                    continue
                if inside:
                    count += t.pos.x - last_pos.x + 1
                last_pos = t.pos
                inside = not inside
            else:
                # we've hit a horizontal trench
                if inside:
                    count += t.pos.x - last_pos.x
                start = self.corners[t.pos]
                count += t.distance + 1
                end = self.corners[t.end]
                # check for lines with opposite pointing ends
                if start == 'F' and end == 'J':
                    inside = not inside
                if start == 'L' and end == '7':
                    inside = not inside
                last_pos = Pos(t.end.x + 1, t.end.y)
        return count
                            

    # Sort the trenches by y, x of their top left, horizontal before vertical
    # pop trenches off the list that cross current line until we find one
    # that doesn't.
    # From this, you can work out how many lines you can scan before
    # you need to change the current set of trenches
    # You can then use the line score x line count to compute efficiently.
    def fill_count(self):
        count = 0
        subcount = 0
        trenches = sorted(self.trenches, key = lambda t: (t.pos.y, t.pos.x, 0 if t.is_vert() else 1), reverse = True)
        # This contains trenches that intersect the current line of interest
        cur = [trenches.pop()]
        cy = cur[0].pos.y
        # It feels like this structure can be simplified
        while cur:
            n = None
            # keep adding trenches that intersect the current line of interest
            if trenches:
                # n is next unsued trench
                n = trenches.pop()
                if n and n.yintersects(cy):
                    cur.append(n)
                    continue
            while cur:
                # how many lava cells in this line?
                subcount = self.line_count(cy, cur)
                # find next line where the structure changes
                ny = min(t.end.y for t in cur)
                # move one line past a horizontal trench
                if ny == cy:
                    ny = cy + 1
                # does the next unused trench intersect the new line of interest
                if n and n.pos.y < ny:
                    ny = n.pos.y
                # We now know how many lines share the same structure
                count += subcount * (ny - cy)
                # rebuild the current set based on what intersects the new line
                cur = [t for t in cur if t.yintersects(ny)]
                cy = ny
                if n and n.pos.y == ny:
                    # if we got to the next unsused trench then add it and
                    # break out to possibly add more
                    cur.append(n)
                    break
                
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

def parse(line: str) -> Move:
    m = re.match(r"([RDLU]) (\d+)", line)
    return Move(dir_map[m[1]], int(m[2]))


lines = map(str.rstrip, sys.stdin)
dig = Dig()

for trench in map(parse, lines):
    dig.dig(trench)

print(dig.fill_count())
