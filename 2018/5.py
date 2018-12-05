#! /usr/bin/env python3

import string

from advent import Inputs


def react(polymer):
    progress = True
    while progress:
        progress = False
        i = len(polymer) - 1
        while i > 0:
            i -= 1
            a, b = polymer[i:i+2]
            if a != b and a.lower() == b.lower():
                del polymer[i:i+2]
                progress = True
                i = min(i, len(polymer) - 1)
    return polymer


polymer = list(Inputs(2018).get(5).text.strip())

print("Part one:", len(react(polymer[:])))


sizes = []
for l in string.ascii_lowercase:
    sizes.append(len(react([c for c in polymer if c.lower() != l])))

print("Part two:", min(sizes))
