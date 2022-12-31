#!/usr/bin/env /usr/bin/python3

import sys
from dataclasses import dataclass, field
from itertools import combinations, count
from heapq import heappush, heappop

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
    floor_count = 4
    floors: tuple
    elevator: int
    moves: int
    score: int = field(init = False)

    def __post_init__(self):
        l = self.floor_count - 1
        object.__setattr__(self, 'score', self.moves + 2 * sum(len(f) * (l - i) for i, f in enumerate(self.floors)))

    # I'm not 100% convinced this guarantees we find the shortest route
    def __lt__(self, other):
        s1, s2 = self.score, other.score
        if s1 == s2:
            return self.moves > other.moves
        else:
            return s1 < s2

    def is_finished(self):
        # Finished if all floors are empty except the last
        return all(not x for x in self.floors[:self.floor_count - 1])

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
                    elevator = self.elevator + 1,
                    moves = self.moves + 1
                )
            if self.elevator > 0:
                # elevator can go down
                yield State (
                    floors = tuple(move(self.floors, items, self.elevator, self.elevator - 1)),
                    elevator = self.elevator - 1,
                    moves = self.moves + 1
                )

def solve(state):
    visited = set()
    states = []
    heappush(states, state)
    while True:
        s = heappop(states)
        if s.is_finished():
            return s
        if not s in visited:
            visited.add(s)
            if s.is_valid():
                for n in s.next_states():
                    heappush(states, n)

example_initial_state = State(
    floors = (
        frozenset([("H", "M"), ("L", "M")]),
        frozenset([("H", "G")]),
        frozenset([("L", "G")]),
        frozenset()
    ),
    elevator = 0,
    moves = 0
)

puzzle_initial_state_1 = State(
    floors = (
        frozenset([("S", "G"), ("S", "M"), ("P", "G"), ("P", "M")]),
        frozenset([("T", "G"), ("R", "G"), ("R", "M"), ("C", "G"), ("C", "M")]),
        frozenset([("T", "M")]),
        frozenset()
    ),
    elevator = 0,
    moves = 0
)

puzzle_initial_state = State(
    floors = (
        frozenset([("S", "G"), ("S", "M"), ("P", "G"), ("P", "M"), ("E", "G"), ("E", "M"), ("D", "G"), ("D", "M")]),
        frozenset([("T", "G"), ("R", "G"), ("R", "M"), ("C", "G"), ("C", "M")]),
        frozenset([("T", "M")]),
        frozenset()
    ),
    elevator = 0,
    moves = 0
)

s = solve(puzzle_initial_state)
print(s.moves)
