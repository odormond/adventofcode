#! /usr/bin/env python

from collections import defaultdict
from pathlib import Path
import advent_of_code as adv

test_data = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


def to_list_of_lines(data):
    return [
        tuple(tuple(map(int, point.split(','))) for point in line.split(' -> '))
        for line in data.splitlines()
    ]


def overlaps(lines, with_diag=False):
    overlaps = 0
    cells = defaultdict(lambda: 0)
    for (x1, y1), (x2, y2) in lines:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                cells[(x1, y)] += 1
                if cells[(x1, y)] == 2:
                    overlaps += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                cells[(x, y1)] += 1
                if cells[(x, y1)] == 2:
                    overlaps += 1
        elif abs(x2 - x1) == abs(y2 - y1) and with_diag:
            s_x = 1 if x1 < x2 else - 1
            s_y = 1 if y1 < y2 else - 1
            for cell in zip(range(x1, x2 + s_x, s_x), range(y1, y2 + s_y, s_y)):
                cells[cell] += 1
                if cells[cell] == 2:
                    overlaps += 1
    return overlaps


assert overlaps(to_list_of_lines(test_data)) == 5
assert overlaps(to_list_of_lines(test_data), True) == 12

lines = adv.input(Path(__file__).parent.name, to_list_of_lines)
print("Part 1:", overlaps(lines))
print("Part 2:", overlaps(lines, True))
