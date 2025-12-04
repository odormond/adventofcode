#! /usr/bin/env python

from itertools import product

import advent_of_code as aoc

test_data = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

def parse(data):
    return {
        (l, c)
        for l, line in enumerate(data.splitlines())
        for c, cell in enumerate(line)
        if cell == "@"
    }, len(data.splitlines()), len(data.splitlines()[0])


def neighbours(l, c):
    for dl, dc in product((-1, 0, 1), repeat=2):
        if (dl, dc) == (0, 0):
            continue
        yield (l + dl, c + dc)


def part1(data):
    rolls, lines, cols = parse(data)
    return sum(
        1
        for l, c in product(range(lines), range(cols))
        if (l, c) in rolls and sum(1 for ll, cc in neighbours(l, c) if (ll, cc) in rolls) < 4
    )


assert (result := part1(test_data)) == 13, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    rolls, lines, cols = parse(data)
    initial = len(rolls)
    while rolls:
        to_remove = {
            (l, c)
            for l, c in product(range(lines), range(cols))
            if (l, c) in rolls and sum(1 for ll, cc in neighbours(l, c) if (ll, cc) in rolls) < 4
        }
        if not to_remove:
            break
        rolls -= to_remove
    return initial - len(rolls)


assert (result := part2(test_data)) == 43, f"{result=}"
print("Part 2:", part2(aoc.input()))
