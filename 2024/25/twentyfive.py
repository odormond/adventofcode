#! /usr/bin/env python

from itertools import product

import advent_of_code as aoc

test_data = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def parse(data):
    locks = []
    keys = []
    for block in data.split("\n\n"):
        lines = block.splitlines()
        if lines[0] == ".....":
            # key
            lines = lines[::-1]
            kind = keys
        else:
            kind = locks
        pins = [0] * 5
        for h, line in enumerate(lines[1:], start=1):
            for p, v in enumerate(line):
                if v == "#":
                    pins[p] = h
        kind.append(pins)
    return locks, keys


def fit(lock, key):
    return all(l + k <= 5 for l, k in zip(lock, key))


def part1(data):
    return sum(1 for lock, key in product(*parse(data)) if fit(lock, key))


assert (result := part1(test_data)) == 3, f"{result=}"
print("Part 1:", part1(aoc.input()))

raise SystemExit()

def part2(data):
    return parse(data)


assert (result := part2(test_data)) == "", f"{result=}"
print("Part 2:", part2(aoc.input()))
