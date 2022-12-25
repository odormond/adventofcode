#! /usr/bin/env python

import advent_of_code as adv

test_data = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

SNAFU_DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
REVERSE_SNAFU_DIGITS = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}


def from_snafu(num):
    result = 0
    for i, c in enumerate(reversed(num)):
        result += SNAFU_DIGITS[c] * 5 ** i
    return result


def to_snafu(num):
    result = []
    i = 0
    while num:
        num, rest = divmod(num, 5)
        if rest > 2:
            num += 1
            rest -= 5
        result.append(REVERSE_SNAFU_DIGITS[rest])
    return ''.join(result[::-1])


def parse(data):
    return [from_snafu(n) for n in data.splitlines()]


def part1(data):
    return to_snafu(sum(parse(data)))


assert (result := part1(test_data)) == "2=-1=0", f"{result=}"
print("Part 1:", part1(adv.input()))
