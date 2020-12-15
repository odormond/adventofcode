#! /usr/bin/env python3

import os.path
import advent_of_code as adv

TESTS = (
    ([0, 3, 6], 2020, 436),
    ([1, 3, 2], 2020, 1),
    ([2, 1, 3], 2020, 10),
    ([1, 2, 3], 2020, 27),
    ([2, 3, 1], 2020, 78),
    ([3, 2, 1], 2020, 438),
    ([3, 1, 2], 2020, 1836),
    ([0, 3, 6], 30000000, 175594),
    ([1, 3, 2], 30000000, 2578),
    ([2, 1, 3], 30000000, 3544142),
    ([1, 2, 3], 30000000, 261214),
    ([2, 3, 1], 30000000, 6895259),
    ([3, 2, 1], 30000000, 18),
    ([3, 1, 2], 30000000, 362),
)


def compile(seq):
    summary = {}
    for i, n in enumerate(seq):
        summary[n] = (summary.get(n, (i, i))[1], i)
    return summary


def next_num(last, n, summary):
    a, b = summary.get(last, (n, n))
    num = b - a
    summary[num] = summary.get(num, (n, n))[1], n
    return num


def run(data, end):
    summary = compile(data)
    num = data[-1]
    n = len(data)
    for i in range(end - len(data)):
        num = next_num(num, n, summary)
        n += 1
    return num


for test, end, expected in TESTS:
    result = run(test, end)
    assert result == expected


data = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_int)
print("Part 1:", run(data, 2020))
print("Part 2:", run(data, 30000000))
