#! /usr/bin/env python

import re

import advent_of_code as adv

test_data = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

def parse(data):
    for line in data.splitlines():
        digits = re.findall(r'\d', line)
        yield int(digits[0] + digits[-1])


def part1(data):
    return sum(parse(data))


assert (result := part1(test_data)) == 142, f"{result=}"
print("Part 1:", part1(adv.input()))


DIGITS_RE = re.compile(r'(\d|one|two|three|four|five|six|seven|eight|nine)')
DIGITS_VALUE = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
} | {str(d): d for d in range(1, 10)}


def parse(data):
    for line in data.splitlines():
        digits = []
        while match := DIGITS_RE.search(line):
            digits.append(DIGITS_VALUE[match.group(1)])
            line = line[1:]
        yield 10 * digits[0] + digits[-1]


def part2(data):
    return sum(parse(data))


test_data = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

assert (result := part2(test_data)) == 281, f"{result=}"
print("Part 2:", part2(adv.input()))
