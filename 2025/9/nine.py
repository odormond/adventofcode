#! /usr/bin/env python

from itertools import combinations

import advent_of_code as aoc

test_data = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

def parse(data):
    return [tuple(int(v) for v in line.split(",")) for line in data.splitlines()]


def part1(data):
    reds = parse(data)
    area = 0
    for (a0, a1), (b0, b1) in combinations(reds, 2):
        area = max(area, abs((a0 - b0 + 1) * (a1 - b1 + 1)))
    return area


assert (result := part1(test_data)) == 50, f"{result=}"
print("Part 1:", part1(aoc.input()))


class Rectangle:
    def __init__(self, a, b):
        self.tl = min(a[0], b[0]), min(a[1], b[1])
        self.br = max(a[0], b[0]), max(a[1], b[1])

    @property
    def area(self):
        return (self.br[0] - self.tl[0] + 1) * (self.br[1] - self.tl[1] + 1)

    def intersect(self, segment):
        (ax, ay), (bx, by) = segment
        tlx, tly = self.tl
        brx, bry = self.br
        if tlx < ax < brx and tly < ay < bry:
            return True  # a inside rect
        if tlx < bx < brx and tly < by < bry:
            return True  # b inside rect
        if ax == bx and tlx < ax < brx and ((ay <= tly and by >= bry) or (by <= tly and ay >= bry)):
            return True  # a-b vertical crossing rect
        if ay == by and tly < ay < bry and ((ax <= tlx and bx >= brx) or (bx <= tlx and ax >= brx)):
            return True  # a-b horizontal crossing rect


def part2(data):
    reds = parse(data)
    segments = [(a, b) for a, b in zip(reds, reds[1:] + reds[:1])]
    area = 0
    for a, b in combinations(reds, 2):
        rect = Rectangle(a, b)
        if any(rect.intersect(segment) for segment in segments):
            continue
        area = max(area, rect.area)
    return area


assert (result := part2(test_data)) == 24, f"{result=}"
print("Part 2:", part2(aoc.input()))
