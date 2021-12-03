#! /usr/bin/env python

from functools import partial
from pathlib import Path
import advent_of_code as adv

test_data = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


def most_least_common(data):
    count = len(data)
    size = len(data[0])
    threshold = count / 2
    gamma = sum((1 if [line[column] for line in data].count("1") >= threshold else 0) << (size - 1 - column) for column in range(size))
    epsilon = gamma ^ ((1 << size) - 1)
    return gamma, epsilon


def power(data):
    gamma, epsilon = most_least_common(data)
    return gamma * epsilon


assert power(adv.to_list_of_str(test_data)) == 198

data = adv.input(Path(__file__).parent.name, adv.to_list_of_str)
print("Part 1:", power(data))


def filter_by_criteria(data, creteria):
    size = len(data[0])
    for bit in range(size):
        if len(data) == 1:
            break
        gamma, epsilon = most_least_common(data)
        most = '1' if gamma & (1 << (size - 1 - bit)) else '0'
        least = '1' if epsilon & (1 << (size - 1 - bit)) else '0'
        data = list(filter(partial(creteria, most, least, bit), data))
    if len(data) == 1:
        return int(data[0], 2)


def oxygen(most, least, bit, data):
    return data[bit] == most


def co2(most, least, bit, data):
    return data[bit] == least


assert filter_by_criteria(adv.to_list_of_str(test_data), oxygen) == 23
assert filter_by_criteria(adv.to_list_of_str(test_data), co2) == 10

print("Part 2:", filter_by_criteria(data, oxygen) * filter_by_criteria(data, co2))
