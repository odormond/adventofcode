#! /usr/bin/env python3

import itertools

from advent import Inputs


def manhattan(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax-bx) + abs(ay-by)


coordinates = [tuple(map(int, l.split(', '))) for l in Inputs(2018).get(6).iter_lines(decode_unicode=True)]

MARGIN = 2
width = max(x for x, y in coordinates) + MARGIN
height = max(y for x, y in coordinates) + MARGIN


grid = [[None for x in range(width)] for y in range(height)]

areas = [0] * len(coordinates)
for x, y in itertools.product(range(width), range(height)):
    distances = sorted((manhattan((x, y), c), i) for i, c in enumerate(coordinates))
    if distances[0][0] < distances[1][0]:
        d, i = distances[0]
        grid[y][x] = i
        areas[i] += 1

for x, y in itertools.chain(itertools.product(range(width), (0, height-1)),
                            itertools.product((0, width-1), range(height))):
    i = grid[y][x]
    if i is not None:
        areas[i] = 0

print("Part one:", max(areas))


size = 0
for x, y in itertools.product(range(width), range(height)):
    total = sum(manhattan((x, y), c) for c in coordinates)
    if total < 10000:
        size += 1

print("Part two:", size)
