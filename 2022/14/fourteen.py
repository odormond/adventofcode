#! /usr/bin/env python

from itertools import product

import advent_of_code as adv

test_data = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

ROCK = '#'
SAND = 'o'
START = 500, 0


def segment(a, b):
    return range(a, b + 1) if a < b else range(b, a + 1)


def to_grid(data):
    grid = {}
    abyss = 0
    for line in data.splitlines():
        px = py = None
        for corner in line.split(' -> '):
            cx, cy = [int(c) for c in corner.split(',')]
            abyss = max(abyss, cy)
            if px is not None:
                for x, y in product(segment(px, cx), segment(py, cy)):
                    grid[(x, y)] = ROCK
            px, py = cx, cy
    return grid, abyss + 1


def one_sand(grid, abyss):
    x, y = START
    while y < abyss:
        if grid.get((x, y)) is not None:
            return False
        if grid.get((x, y + 1)) is None:
            y += 1
        elif grid.get((x - 1, y + 1)) is None:
            x -= 1
            y += 1
        elif grid.get((x + 1, y + 1)) is None:
            x += 1
            y += 1
        else:
            grid[(x, y)] = SAND
            return True
    return False


def simulate(grid, abyss):
    resting = 0
    while one_sand(grid, abyss):
        resting += 1
    return resting


def part1(data):
    grid, abyss = to_grid(data)
    return simulate(grid, abyss)


def part2(data):
    grid, abyss = to_grid(data)
    for x in segment(START[0] - abyss - 2, START[0] + abyss + 2):
        grid[(x, abyss + 1)] = ROCK
    return simulate(grid, abyss + 2)


assert (result := part1(test_data)) == 24, f"{result=}"
print("Part 1:", part1(adv.input()))

assert (result := part2(test_data)) == 93, f"{result=}"
print("Part 2:", part2(adv.input()))
