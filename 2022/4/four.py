#! /usr/bin/env python

import advent_of_code as adv


test_data = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def to_pair_of_sections(data):
    return [
        tuple(
            tuple(int(i) for i in section.split('-'))
            for section in pair.split(',')
        )
        for pair in data.splitlines()
    ]


def overlaps(assignments, test):
    return sum(1 for (a, b), (x, y) in assignments if test(a, b, x, y))


def part1(assignments):
    return overlaps(
        assignments,
        lambda a, b, x, y: (a <= x <= b and a <= y <= b) or (x <= a <= y and x <= b <= y)
    )


test_assignments = to_pair_of_sections(test_data)
assignments = to_pair_of_sections(adv.input())

assert part1(test_assignments) == 2
print("Part 1:", part1(assignments))

def part2(assignments):
    return overlaps(
        assignments,
        lambda a, b, x, y: a <= x <= b or a <= y <= b or x <= a <= y or x <= b <= y
    )


assert part2(test_assignments) == 4
print("Part 2:", part2(assignments))
