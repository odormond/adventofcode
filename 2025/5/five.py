#! /usr/bin/env python

import advent_of_code as aoc

test_data = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

def parse(data):
    lines = data.splitlines()
    fresh_ranges = []
    while (line := lines.pop(0)):
        low, hi = line.split("-")
        fresh_ranges.append((int(low), int(hi)))
    availables = [int(line) for line in lines]
    return fresh_ranges, availables


def part1(data):
    freshes, availables = parse(data)
    return sum(
        1 for ingredient in availables if any(low <= ingredient <= hi for low, hi in freshes)
    )


assert (result := part1(test_data)) == 3, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    freshes, _ = parse(data)
    freshes = sorted(freshes)
    optimized = [freshes.pop(0)]
    while freshes:
        opt_low, opt_hi = optimized[-1]
        low, hi = freshes.pop(0)
        if low <= opt_hi:
            if hi > opt_hi:
                optimized[-1] = (opt_low, hi)
        else:
            optimized.append((low, hi))
    return sum(hi - low + 1 for low, hi in optimized)


assert (result := part2(test_data)) == 14, f"{result=}"
print("Part 2:", part2(aoc.input()))
