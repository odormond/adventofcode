#! /usr/bin/env python3

import collections
import itertools

from advent import Inputs

source = Inputs(2018).get(18).text

tsource = """\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""

area = [list(line.strip()) for line in source.splitlines()]
SIDE = len(area)


def characterize(area):
    s = '\n'.join(''.join(line) for line in area)
    return hash(s), s.count('|'), s.count('#')


NEIGHBOURS = [
    [[(0, 1), (1, 0), (1, 1)]]  # top-left corner
    + [[(0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]] * (SIDE-2)  # top edge
    + [[(0, -1), (1, -1), (1, 0)]]  # top-right corner
]
NEIGHBOURS += [
    [[(-1, 0), (-1, 1), (0, 1), (1, 0), (1, 1)]]  # left edge
    + [[pos for pos in itertools.product((-1, 0, 1), repeat=2) if pos != (0, 0)]] * (SIDE-2)  # center
    + [[(-1, -1), (-1, 0), (0, -1), (1, -1), (1, 0)]]  # right edge
] * (SIDE-2)
NEIGHBOURS += [
    [[(-1, 0), (-1, 1), (0, 1)]]  # bottom-left corner
    + [[(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]] * (SIDE-2)  # bottom edge
    + [[(-1, -1), (-1, 0), (0, -1)]]  # bottom-right corner
]


def count_types(area, y, x):
    counts = {'.': 0, '|': 0, '#': 0}
    for dy, dx in NEIGHBOURS[y][x]:
        ty, tx = y+dy, x+dx
        counts[area[ty][tx]] += 1
    return counts['|'], counts['#']


def evolve(minutes, area, seen):
    next_area = [line[:] for line in area]
    for i in range(minutes):
        for y, x in itertools.product(range(SIDE), repeat=2):
            t, l = count_types(area, y, x)
            a = area[y][x]
            if a == '.' and t >= 3:
                next_area[y][x] = '|'
            elif a == '|' and l >= 3:
                next_area[y][x] = '#'
            elif a == '#' and not (t >= 1 and l >= 1):
                next_area[y][x] = '.'
            else:
                next_area[y][x] = area[y][x]
        area, next_area = next_area, area
        h, t, l = characterize(area)
        if h in seen:
            start = list(seen).index(h)
            print("Cycle detected!!", t*l, i, start, i-start)
            return start, i-start
        seen[h] = t*l
    return area


seen = collections.OrderedDict()
area = evolve(10, area, seen)

print("Part one:", list(seen.values())[-1])

area = [list(line.strip()) for line in source.splitlines()]
seen = collections.OrderedDict()
target = 1000000000
start, length = evolve(target, area, seen)
solution = start + ((target - 1 - start) % length)

print("Part two:", list(seen.items())[solution][1])
