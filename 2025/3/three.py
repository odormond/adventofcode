#! /usr/bin/env python

import advent_of_code as aoc

test_data = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""

def parse(data):
    return [[int(b) for b in bank] for bank in data.splitlines()]


def solver(data, count=2):
    total = 0
    for bank in parse(data):
        batteries = []
        start_idx = 0
        for i in range(count):
            end_idx = len(bank) - count + i + 1
            hi = max(bank[start_idx:end_idx])
            start_idx = bank[:end_idx].index(hi, start_idx) + 1
            batteries.append(hi)
        total += sum(b * 10**i for i, b in enumerate(reversed(batteries)))
    return total


assert (result := solver(test_data)) == 357, f"{result=}"
print("Part 1:", solver(aoc.input()))


assert (result := solver(test_data, 12)) == 3121910778619, f"{result=}"
print("Part 2:", solver(aoc.input(), 12))
