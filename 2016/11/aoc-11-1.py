#!/usr/bin/env /usr/bin/python3

import sys
from dataclasses import dataclass
from itertools import combinations, count

def combinations_range(seq, r):
    for i in r:
        yield from combinations(seq, i)

def move(floors, items, src, dst):
    for i, f in enumerate(floors):
        if i == src:
            yield f - items
        elif i == dst:
            yield f | items
        else:
            yield f

@dataclass(frozen = True)
class State:
    # tuple of frozen set to make hashing easy
    floors: tuple
    elevator: int

    def is_finished(self):
        # Finished if all floors are empty except the last
        c = len(self.floors)
        return all(not x for x in self.floors[:c - 1])

    def is_valid(self):
        # invalid state if we have a floor with a chip
        # without its RTG and with a different one
        for floor in self.floors:
            chips = [x for x, t in floor if t == "M"]
            rtgs = [x for x, t in floor if t == "G"]
            if any(c for c in chips if c not in rtgs and any(rtgs)):
                return False
        return True

    def next_states(self):
        # elevator can take one or two (but not zero) items
        # up or down one floor
        # we know there will always be at least one available
        # as we always have the last thing transferred available
        for items in combinations_range(self.floors[self.elevator], [1, 2]):
            items = set(items)
            if self.elevator < len(self.floors) - 1:
                # elevator can go up
                yield State (
                    floors = tuple(move(self.floors, items, self.elevator, self.elevator + 1)),
                    elevator = self.elevator + 1
                )
            if self.elevator > 0:
                # elevator can do down
                yield State (
                    floors = tuple(move(self.floors, items, self.elevator, self.elevator - 1)),
                    elevator = self.elevator - 1
                )

def solve(state):
    visited = set()
    starts = {state}
    for i in count():
        new_starts = set()
        for s in starts:
            if s.is_finished():
                return i
            if not s in visited:
                visited.add(s)
                if s.is_valid():
                    new_starts.update(s.next_states())
        if not new_starts:
            raise Exception("No solution")
        starts = new_starts

example_initial_state = State(
    floors = (
        frozenset([("H", "M"), ("L", "M")]),
        frozenset([("H", "G")]),
        frozenset([("L", "G")]),
        frozenset()
    ),
    elevator = 0
)

puzzle_initial_state = State(
    floors = (
        frozenset([("S", "G"), ("S", "M"), ("P", "G"), ("P", "M")]),
        frozenset([("T", "G"), ("R", "G"), ("R", "M"), ("C", "G"), ("C", "M")]),
        frozenset([("T", "M")]),
        frozenset()
    ),
    elevator = 0
)

print(solve(puzzle_initial_state))
