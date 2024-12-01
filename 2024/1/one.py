#! /usr/bin/env python

from collections import Counter

import advent_of_code as aoc

test_data = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""

def parse(data):
    data = [[int(i) for i in line.split()] for line in data.splitlines()]
    return list(zip(*data))


def part1(data):
    left, right = parse(data)
    return sum(abs(a - b) for a, b in zip(sorted(left), sorted(right)))


assert (result := part1(test_data)) == 11, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    left, right = parse(data)
    right_cnt = Counter(right)
    return sum(right_cnt.get(l, 0) * l for l in left)


assert (result := part2(test_data)) == 31, f"{result=}"
print("Part 2:", part2(aoc.input()))
