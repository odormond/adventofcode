#! /usr/bin/env python3

import itertools
import advent_of_code as adv


expenses = adv.input(1, adv.to_list_of_int)

for a, b in itertools.combinations(expenses, 2):
    if a + b == 2020:
        print("Part 1:", a * b)
        break

for a, b, c in itertools.combinations(expenses, 3):
    if a + b + c == 2020:
        print("Part 2:", a * b * c)
        break
