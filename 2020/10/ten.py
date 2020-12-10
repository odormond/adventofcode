#! /usr/bin/env python3

from collections import Counter
import os.path
import advent_of_code as adv


TEST_1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
TEST_2 = [
    28,
    33,
    18,
    42,
    31,
    14,
    46,
    20,
    48,
    47,
    24,
    23,
    49,
    45,
    19,
    38,
    39,
    11,
    1,
    32,
    25,
    35,
    8,
    17,
    7,
    9,
    4,
    2,
    34,
    10,
    3,
]


def jolts_diffs(adapters):
    diffs = Counter()
    prev_output = 0
    for adapter in sorted(adapters):
        diffs[adapter - prev_output] += 1
        prev_output = adapter
    diffs[3] += 1  # device internal adapter
    return diffs


assert jolts_diffs(TEST_1) == Counter({1: 7, 3: 5})
assert jolts_diffs(TEST_2) == Counter({1: 22, 3: 10})

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_int)
diffs = jolts_diffs(data)
print("Part 1:", diffs[1] * diffs[3])


def jolts_arrangements(adapters):
    adapters = adapters[:]
    options = [[adapters.pop(0)]]
    while adapters:
        adapter = adapters.pop(0)
        new_options = []
        for option in options[:]:
            if adapter - option[-1] < 3:
                # Still a chance to plug another adapter
                new_options.append(option)
            if option[-1] + 1 <= adapter <= option[-1] + 3:
                # can plug this adapter -> one more option
                new_options.append(option + [adapter])
        options = new_options
    # Keep only options that uses the largest adapter, which is the last one
    options = list(filter(lambda o: o[-1] == adapter, options))
    return len(options)


def skippable(adapters):
    N = len(adapters)
    skips = []
    for i in range(N - 3):
        a, b, c, d = adapters[i : i + 4]
        if a + 3 == b:
            # No skip possible
            continue
        skip = 0
        if a + 3 == c or a + 2 == c:
            # We can skip b
            skip += 1
        if a + 3 == d:
            # We can skip both b and c
            skip += 1
        if skip:
            skips.append((i, skip))
    return skips


def overlaps(skips):
    low, length = skips.pop(0)
    segments = [(low, low + length + 1)]
    while skips:
        low, hi = segments[-1]
        next, length = skips.pop(0)
        if next < hi:
            segments[-1] = (low, next + length + 1)
        else:
            segments.append((next, next + length + 1))
    return segments


def count_arrangements(adapters):
    adapters = sorted([0] + adapters)
    skips = skippable(adapters)
    overs = overlaps(skips[:])
    product = 1
    for low, hi in overs:
        product *= jolts_arrangements(adapters[low : hi + 1])
    return product


for test, expected in ((TEST_1, 8), (TEST_2, 19208)):
    assert expected == count_arrangements(test)

print("Part 2:", count_arrangements(data))
