#!/usr/bin/env python3

import sys
from dataclasses import dataclass

# by inspection, we start from the centre of the map, which is square
# there are clear lines north, east, west and south.
# there are also clear boundaries around the edge
# So, map copies in cardinal directions will always fill from
# the centre of the adjacent edge
# all other map copies will fill from the corner closest to the start.
# Reachable cells will alternate diagonals as the number of moves is odd or even
# For each of the ingress points, we can work out many moves it takes to cover
# the tile
# The map is a square of 131 x 131, start is at the centre.
# So after 66 moves, we hit the cardinally adjacent maps
# after 132, we hit the corners of the the diagonally adjacent maps
# after 66+132, we hit the next cardinally adjacent maps
# after 132+132, we hit eight more diagnonally adjacent maps, two in each diagonal
# after n moves, we therefor hit in each diagnonal
# 1 diagonal after n - 132
# 2 diagonals after n - 132 - 132
# x diagonals after n - 132x
# as long as 132x > n
# Simlarly
# 1 cardinal after n - 66
# 2 cardinals after n - 66 - 132
# x cardinals after n - 66 - (x- 1)132
# as long as 132x + 66 > n

class Layout:
    cells: list[str]
    width: int
    height: int
    # frontier_sizes is a mapping from (startx, starty), move count -> frontier size
    # For as long as the frontier doesn't get to it's end point where it starts
    # alternating diagonals
    frontier_sizes: dict[((int, int), int), int]
    # frontier_ends says what is the last move count in the above dict for each start
    frontier_ends: dict[(int, int), int]

    def __init__(self, cells):
        self.cells = list(cells)
        self.width = len(self.cells[0])
        self.height = len(self.cells)
        f = self.width - 1
        h = f // 2
        ingress_points = [(0, 0), (0, h), (0, f), (h, 0), (h, h), (h, f), (f, 0), (f, h), (f, f)]
        self.compute_frontiers(ingress_points)

    def compute_frontiers(self, ingress_points):
        self.frontier_sizes = {}
        self.frontier_ends = {}
        for pos in ingress_points:
            move_count = 0
            frontier = {pos}
            frontiers = []
            while frontier not in frontiers:
                frontiers.append(frontier)
                self.frontier_sizes[(pos, move_count)] = len(frontier)
                move_count += 1
                frontier = self.expand_frontier(frontier)
            self.frontier_ends[pos] = move_count

    def expand_frontier(self, frontier):
        new_frontier = set()
        for pos in frontier:
            new_frontier.update(self.open_neighbours(pos))
        return new_frontier

    def start(self):
        for y in range(self.height):
            if 'S' in self.cells[y]:
                return self.cells[y].index('S'), y
        raise ValueError("Could not find Start")

    def in_bounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def is_garden(self, x, y):
        return self.in_bounds(x, y) and self.cells[y][x] != '#'

    def open_neighbours(self, pos):
        x, y = pos
        for (i, j) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if self.is_garden(x + i, y + j):
                yield x + i, y + j

    # how big is the frontier after moves, just looking at one tile
    def frontier_size_tile(self, start, moves):
        end = self.frontier_ends[start]
        if moves < end:
            return self.frontier_sizes[(start, moves)]
        elif moves % 2 == end % 2:
            return self.frontier_sizes[(start, end - 2)]
        else:
            return self.frontier_sizes[(start, end - 1)]

    def frontier_size(self, moves):
        f = self.width - 1
        h = f // 2
        # how much of the initial tile to we hit?
        tot = self.frontier_size_tile((h, h), moves)

        cardinal_points = [(0, h), (h, 0), (h, f), (f, h)]
        diagonal_points = [(0, 0), (0, f), (f, 0), (f, f)]

        for pos in cardinal_points:
            end = self.frontier_ends[pos]
            number_of_tiles = (moves + h) // (f + 1)
            moves_in_last_tile = (moves + h) % (f + 1)
            while number_of_tiles > 0:
                # There's room for improvement here
                # see whether all remaining tiles have reached their end state
                # and multiply out etc
                tot += self.frontier_size_tile(pos, moves_in_last_tile)
                moves_in_last_tile += f + 1
                number_of_tiles -= 1

        for pos in diagonal_points:
            end = self.frontier_ends[pos]
            number_of_tiles = (moves - 1) // (f + 1)
            moves_in_last_tile = (moves - 1) % (f + 1)
            # on the diagnonal we get more tiles 
            while number_of_tiles > 0:
                # same as cardinals, we can multiply out
                tot += number_of_tiles * self.frontier_size_tile(pos, moves_in_last_tile)
                moves_in_last_tile += f + 1
                number_of_tiles -= 1

        return tot;

layout = Layout(map(str.rstrip, sys.stdin))

print(layout.frontier_size(26501365))
