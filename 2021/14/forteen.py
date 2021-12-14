#! /usr/bin/env python

from collections import Counter
from itertools import pairwise, product
from pathlib import Path
import advent_of_code as adv


def parse(text):
    template, insertions = text.strip().split('\n\n')
    rules = {}
    for rule in insertions.splitlines():
        k, v = rule.split(' -> ')
        rules[tuple(k)] = v
    return template, rules


test_data = parse((Path(__file__).parent / 'test_data').read_text())
data = adv.input(Path(__file__).parent.name, parse)


def apply(template, rules):
    result = []
    for pair in pairwise(list(template)):
        result += [pair[0], rules[pair]]
    result.append(pair[-1])
    return ''.join(result)


def checksum(polymer):
    counts = Counter(polymer).most_common()
    most, most_count = counts[0]
    least, least_count = counts[-1]
    return most_count - least_count


polymer, rules = test_data
assert (polymer := apply(polymer, rules)) == 'NCNBCHB'
assert (polymer := apply(polymer, rules)) == 'NBCCNBBBCBHCB'
assert (polymer := apply(polymer, rules)) == 'NBBBCNCCNBBNBNBBCHBHHBCHB'
assert (polymer := apply(polymer, rules)) == 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
assert len(polymer := apply(polymer, rules)) == 97
for i in range(5):
    polymer = apply(polymer, rules)
assert len(polymer) == 3073
assert polymer.count('B') == 1749
assert polymer.count('C') == 298
assert polymer.count('H') == 161
assert polymer.count('N') == 865
assert checksum(polymer) == 1588
foo = polymer

polymer, rules = data
for i in range(10):
    polymer = apply(polymer, rules)
print("Part 1:", checksum(polymer))


def parse2(text):
    template, insertions = text.strip().split('\n\n')
    rules = {}
    for rule in insertions.splitlines():
        k, v = rule.split(' -> ')
        rules[k] = v
    polymer = Counter(a+b for a,b in pairwise(template))
    return polymer, rules


def apply2(polymer, rules):
    updated = {}
    for pair, count in polymer.items():
        a, b = tuple(pair)
        insert = rules[pair]
        updated[a + insert] = updated.get(a + insert, 0) + count
        updated[insert + b] = updated.get(insert + b, 0) + count
    return updated


def checksum2(polymer):
    first = set(pair[0] for pair in polymer)
    second = set(pair[1] for pair in polymer)
    counts = Counter({letter: sum(polymer.get(a + letter, 0) for a in first) for letter in second}).most_common()
    most, most_count = counts[0]
    least, least_count = counts[-1]
    return most_count - least_count


test_data2 = parse2((Path(__file__).parent / 'test_data').read_text())
data2 = adv.input(Path(__file__).parent.name, parse2)
polymer, rules = test_data2
for i in range(40):
    polymer = apply2(polymer, rules)
assert checksum2(polymer) == 2188189693529

polymer, rules = data2
for i in range(40):
    polymer = apply2(polymer, rules)
print("Part 2:", checksum2(polymer))
