#! /usr/bin/env python3

import itertools
import os.path
import advent_of_code as adv


TEST = """
.#.
..#
###
"""


class Space:
    def __init__(self, text, n_dim=3):
        self.n_dim = n_dim
        self.space = {}
        for y, line in enumerate(text.strip().splitlines()):
            for x, state in enumerate(line):
                if state == '#':
                    self.space[(x, y) + (0,) * (n_dim - 2)] = 1
        self.update_bounds()

    def interate(self):
        space = {}
        for pos in itertools.product(
            *(range(self.min[axis] - 1, self.max[axis] + 2) for axis in range(self.n_dim))
        ):
            is_active = self.space.get(pos, 0)
            neighbours = self.count_neighbours(pos)
            if (is_active and neighbours in (2, 3)) or (not is_active and neighbours == 3):
                space[pos] = 1

        self.space = space
        self.update_bounds()

    def update_bounds(self):
        occupied = list(self.space)
        self.min = list(occupied.pop(0))
        self.max = self.min[:]
        while occupied:
            for axis, value in enumerate(occupied.pop(0)):
                if value < self.min[axis]:
                    self.min[axis] = value
                if value > self.max[axis]:
                    self.max[axis] = value

    def count_neighbours(self, pos):
        count = 0
        for npos in itertools.product(*(range(d - 1, d + 2) for d in pos)):
            if npos == pos:
                continue
            count += self.space.get(npos, 0)
        return count

    def __str__(self):
        out = []
        for z in range(self.min[2], self.max[2] + 1):
            out.append(f"{z=}\n")
            for y in range(self.min[1], self.max[1] + 1):
                for x in range(self.min[0], self.max[0] + 1):
                    out.append('#' if (x, y, z) in self.space else '.')
                out.append('\n')
            out.append('\n')
        return ''.join(out)


space = Space(TEST)
for i in range(6):
    space.interate()
assert len(space.space) == 112

space = Space(TEST, 4)
for i in range(6):
    space.interate()
assert len(space.space) == 848

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), str)
space = Space(data)
for i in range(6):
    space.interate()
print("Part 1:", len(space.space))

space = Space(data, 4)
for i in range(6):
    space.interate()
print("Part 2:", len(space.space))
