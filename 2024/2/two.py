#! /usr/bin/env python

from itertools import pairwise

import advent_of_code as aoc

test_data = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

def parse(data):
    return [
        [int(level) for level in line.split()]
        for line in data.splitlines()
    ]


def is_safe(report):
    increasing = report[0] < report[1]
    for a, b in pairwise(report):
        delta = b - a
        if delta not in (-3, -2, -1, 1, 2, 3):
            return False
        elif (delta > 0) ^ increasing:
            return False
    return True


def part1(data):
    return len([r for r in parse(data) if is_safe(r)])


assert (result := part1(test_data)) == 2, f"{result=}"
print("Part 1:", part1(aoc.input()))


def is_safe_tolerant(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True
    return False


def part2(data):
    return len([r for r in parse(data) if is_safe_tolerant(r)])


assert (result := part2(test_data)) == 4, f"{result=}"
print("Part 2:", part2(aoc.input()))
