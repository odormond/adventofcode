#! /usr/bin/env python

import advent_of_code as aoc

test_data = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

def parse(data):
    return [int(line.replace("L", "-").replace("R", "")) for line in data.splitlines()]


def part1(data, start=50):
    count = 0
    value = start
    for delta in parse(data):
        value = (value + delta) % 100
        if value == 0:
            count += 1
    return count


assert (result := part1(test_data)) == 3, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data, start=50):
    count = 0
    value = start
    for delta in parse(data):
        ticks, new_value = divmod((value + delta), 100)
        count += abs(ticks)
        if delta < 0:
            count += (1 if new_value == 0 else 0) + (-1 if value == 0 else 0)
        value = new_value
    return count


assert (result := part2(test_data)) == 6, f"{result=}"
print("Part 2:", part2(aoc.input()))
