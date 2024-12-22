#! /usr/bin/env python

import advent_of_code as aoc

test_data = """\
1
10
100
2024
"""


def parse(data):
    return aoc.to_list_of_int(data)


def mix(a, b):
    return a ^ b


def prune(a):
    return a % 16777216


def next_secret(secret):
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))
    return secret



def nth_secret(secret, nth):
    for _ in range(nth):
        secret = next_secret(secret)
    return secret


def part1(data, nth):
    return sum(nth_secret(secret, nth) for secret in parse(data))


assert (result := part1(test_data, 2000)) == 37327623, f"{result=}"
print("Part 1:", part1(aoc.input(), 2000))


test_data = """\
1
2
3
2024
"""


def buyers_data(secret, count):
    prices = []
    changes = []
    prev_price = secret % 10
    for _ in range(count):
        secret = next_secret(secret)
        price = secret % 10
        prices.append(price)
        changes.append(price - prev_price)
        prev_price = price
    windows = {}
    for i, window in enumerate(zip(changes, changes[1:], changes[2:], changes[3:]), start=3):
        if window not in windows:
            windows[window] = i
    return prices, windows


def part2(data, count):
    buyers = [buyers_data(secret, count) for secret in parse(data)]
    sequences = set()
    for _, windows in buyers:
        sequences.update(windows)
    most_bananas = 0
    t = len(sequences)
    for s, seq in enumerate(sequences):
        bananas = 0
        for prices, windows in buyers:
            if seq in windows:
                bananas += prices[windows[seq]]
        most_bananas = max(most_bananas, bananas)
    return most_bananas


assert (result := part2(test_data, 2000)) == 23, f"{result=}"
print("Part 2:", part2(aoc.input(), 2000))
