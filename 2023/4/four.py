#! /usr/bin/env python

import re

import advent_of_code as adv

test_data = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def parse(data):
    for line in data.splitlines():
        card, *numbers = re.findall(r'\d+|\|', line)
        separator = numbers.index('|')
        winners = set(numbers[:separator])
        draws = set(numbers[separator + 1:])
        yield card, winners, draws


def part1(data):
    return sum((1 << len(draws & winners)) >> 1 for card, winners, draws in parse(data))


assert (result := part1(test_data)) == 13, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    cards = [(1, len(draws & winners)) for card, winners, draws in parse(data)]
    for i in range(len(cards)):
        count, wins = cards[i]
        for _ in range(count):
            for j in range(i + 1, i + 1 + wins):
                if j >= len(cards):
                    break
                other_count, other_wins = cards[j]
                cards[j] = other_count + 1, other_wins
    return sum(count for count, _ in cards)


assert (result := part2(test_data)) == 30, f"{result=}"
print("Part 2:", part2(adv.input()))
