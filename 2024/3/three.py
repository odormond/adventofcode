#! /usr/bin/env python

import re

import advent_of_code as aoc

MUL_RE = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

test_data = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

def parse(data):
    return data


def part1(data):
    start = 0
    total = 0
    while match := MUL_RE.search(data, start):
        total += int(match.group(1)) * int(match.group(2))
        start = match.end()
    return total


assert (result := part1(test_data)) == 161, f"{result=}"
print("Part 1:", part1(aoc.input()))


test_data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
OP_MUL_RE = re.compile(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)")

def part2(data):
    enabled = True
    start = 0
    total = 0
    while match := OP_MUL_RE.search(data, start):
        match match.group(0):
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                if enabled:
                    total += int(match.group(1)) * int(match.group(2))
        start = match.end()
    return total


assert (result := part2(test_data)) == 48, f"{result=}"
print("Part 2:", part2(aoc.input()))
