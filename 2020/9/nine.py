#! /usr/bin/env python3

import itertools
import os.path
import advent_of_code as adv


TEST = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]


def find_breach(data, preamble_size):
    for i in range(preamble_size, len(data)):
        target = data[i]
        for a, b in itertools.combinations(data[i - preamble_size : i], 2):
            if a != b and a + b == target:
                break
        else:
            return i, target
    return None


def find_weakness(data, index):
    target = data[index]
    for low, hi in itertools.combinations(range(index), 2):
        chunk = data[low:hi]
        if sum(chunk) == target:
            return min(chunk) + max(chunk)


assert find_breach(TEST, 5)[1] == 127
assert find_weakness(TEST, find_breach(TEST, 5)[0]) == 62

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_int)
index, break_code = find_breach(data, 25)
print("Part 1:", break_code)
print("Part 2:", find_weakness(data, index))
