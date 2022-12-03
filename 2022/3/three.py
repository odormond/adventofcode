#! /usr/bin/env python

import string

import advent_of_code as adv


test_data = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

def to_rucksacks(data):
    for rucksack in data.splitlines():
        yield (rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:])


def missplaced_items(rucksack):
    a, b = rucksack
    common = set(a).intersection(b)
    assert len(common) == 1
    return common.pop()


def item_priority(i):
    if 'a' <= i <= 'z':
        return ord(i) - ord('a') + 1
    else:
        return ord(i) - ord('A') + 27


def part1(data):
    return sum(
        item_priority(missplaced_items(rucksack))
        for rucksack in to_rucksacks(data)
    )


assert part1(test_data) == 157
print("Part 1:", part1(adv.input()))


def badges(rucksacks):
    for group in zip(*([iter(rucksacks)] * 3)):
        common = set(string.ascii_letters)
        for rucksack in group:
            a, b = rucksack
            common.intersection_update(a + b)
        assert len(common) == 1
        yield common.pop()
            

def part2(data):
    return sum(item_priority(badge) for badge in badges(to_rucksacks(data)))


assert part2(test_data) == 70
print("Part 2:", part2(adv.input()))
