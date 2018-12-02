#! /usr/bin/env python3

import itertools
import string

from advent import Inputs


IDs = list(Inputs(2018).get(2).iter_lines(decode_unicode=True))


def two_three(ID):
    letters = {}
    others = {}
    for l in ID:
        if l in string.ascii_lowercase:
            letters[l] = letters.get(l, 0) + 1
        else:
            others[l] = others.get(l, 0) + 1
    if others:
        print("others:", others)
    return any(v == 2 for v in letters.values()), any(v == 3 for v in letters.values())


twos = threes = 0

for ID in IDs:
    two, three = two_three(ID)
    if two:
        twos += 1
    if three:
        threes += 1

print("Part one:", twos * threes)


COUNT = len(IDs[0])

matches = []
for a, b in itertools.combinations(IDs, 2):
    diff = ''.join('^' if x != y else ' ' for x, y in zip(a, b))
    if diff.count('^') == 1:
        matches.append((a, b, diff))

assert len(matches) == 1, matches
a, b, diff = matches[0]
c = diff.index('^')
print("Part two:", a[:c] + a[c+1:], f'\n{a}\n{b}\n{diff}')
