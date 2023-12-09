#! /usr/bin/env python

from functools import reduce
from itertools import pairwise
from operator import add

import advent_of_code as adv

test_data = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

def parse(data):
    for line in data.splitlines():
        yield [int(v) for v in line.split()]


def rsub(a, b):
    return b - a


def predictions(data, reverse=False):
    current_index = 0 if reverse else -1
    for history in data:
        deltas = [history[current_index]]
        while True:
            delta = [b - a for a, b in pairwise(history)]
            deltas.insert(0, delta[current_index])
            if set(delta) == {0}:
                break
            history = delta
        yield reduce(rsub if reverse else add, deltas)


def part1(data):
    return sum(predictions(parse(data)))


assert (result := part1(test_data)) == 114, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    return sum(predictions(parse(data), reverse=True))


assert (result := part2(test_data)) == 2, f"{result=}"
print("Part 2:", part2(adv.input()))
