#! /usr/bin/env python

from functools import cache
import re

import advent_of_code as aoc

test_data = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

def parse(data):
    availables, desired = data.split("\n\n")
    availables = availables.split(", ")
    desired = desired.splitlines()
    return availables, desired


def part1(data):
    availables, desired = parse(data)
    possible_re = re.compile("^(" + "|".join(availables) + ")*$")
    return sum(1 for design in desired if possible_re.match(design))


assert (result := part1(test_data)) == 6, f"{result=}"
print("Part 1:", part1(aoc.input()))


@cache
def arrangements(design, availables):
    count = 0
    for avail in availables:
        if design == avail:
            count += 1
        if design.startswith(avail) and (a := arrangements(design[len(avail):], availables)):
            count += a
    return count


def part2(data):
    availables, desired = parse(data)
    return sum(arrangements(design, tuple(availables)) for design in desired)

assert (result := part2(test_data)) == 16, f"{result=}"
print("Part 2:", part2(aoc.input()))
