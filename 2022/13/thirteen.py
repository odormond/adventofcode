#! /usr/bin/env python

from functools import cmp_to_key
from itertools import chain, zip_longest
import re

import advent_of_code as adv


SAFE_RE = re.compile(r'[,\[\]0-9]+')

test_data = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


def parse(data):
    for pair in data.split('\n\n'):
        left, right = pair.splitlines()
        assert SAFE_RE.match(left) and SAFE_RE.match(right)
        yield eval(left), eval(right)


def compare(left, right):
    match left, right:
        case _, None:
            return +1
        case None, _:
            return -1
        case [*l], [*r]:
            for u, v in zip_longest(l, r):
                c = compare(u, v)
                if c != 0:
                    return c
            return 0
        case [], n:
            return -1
        case n, []:
            return 1
        case [l], n:
            return compare(l, n)
        case [l, *_], n:
            return compare(l, n) or +1
        case n, [r]:
            return compare(n, r)
        case n, [r, *_]:
            return compare(n, r) or -1
        case a, b:
            return -1 if a < b else (+1 if a > b else 0)
        case _:
            assert False, "Unexpected configuration"


def part1(data):
    return sum(i for i, (left, right) in enumerate(parse(data), 1) if compare(left, right) < 1)


assert (result := part1(test_data)) == 13, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    divider_packets = ([[2]], [[6]])
    packets = chain.from_iterable((chain.from_iterable(parse(data)), divider_packets))
    decoder_key = 1
    for i, packet in enumerate(sorted(packets, key=cmp_to_key(compare)), 1):
        if packet in divider_packets:
            decoder_key *= i
    return decoder_key


assert (result := part2(test_data)) == 140, f"{result=}"
print("Part 2:", part2(adv.input()))
