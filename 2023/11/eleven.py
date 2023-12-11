#! /usr/bin/env python

from itertools import combinations

import advent_of_code as adv

test_data = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

def parse(data):
    return [[c for c in line] for line in data.splitlines()]


def find_expansions(universe):
    expanded_lines = {l for l, line in enumerate(universe) if set(line) == {'.'}}
    expanded_cols = {
        c
        for c in range(len(universe[0]))
        if all(line[c] == '.' for line in universe)
    }
    return expanded_lines, expanded_cols


def expanded_manhatan(a, b, expansions, expand_by):
    line_expansions, col_expansions = expansions
    ax, ay = a
    bx, by = b
    ax, bx = sorted([ax, bx])
    ay, by = sorted([ay, by])
    x_expansions = len([x for x in range(ax + 1, bx) if x in col_expansions])
    y_expansions = len([y for y in range(ay + 1, by) if y in line_expansions])
    return bx - ax + by - ay + expand_by * (x_expansions + y_expansions)


def analysis(data, expand_by):
    universe = parse(data)
    expansions = find_expansions(universe)
    galaxies = [
        (x, y)
        for y, line in enumerate(universe)
        for x, cell in enumerate(line)
        if cell == '#'
    ]
    return sum(expanded_manhatan(a, b, expansions, expand_by) for a, b in combinations(galaxies, r=2))


assert (result := analysis(test_data, 1)) == 374, f"{result=}"
print("Part 1:", analysis(adv.input(), 1))


assert (result := analysis(test_data, 9)) == 1030, f"{result=}"
assert (result := analysis(test_data, 99)) == 8410, f"{result=}"
print("Part 2:", analysis(adv.input(), 999999))
