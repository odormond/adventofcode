#! /usr/bin/env python

from collections import Counter
from pathlib import Path
import advent_of_code as adv

SPAWN_INTERVAL = 7
START_SHIFT = 2

test_data = [3, 4, 3, 1, 2]

data = adv.input(Path(__file__).parent.name, adv.to_list_of_int)


def evolve(fishes, days):
    by_age = dict(Counter(fishes))
    for day in range(days):
        next_cycle = {}
        for age in range(SPAWN_INTERVAL + START_SHIFT - 1, -1, -1):
            count = by_age.get(age, 0)
            if age == 0:
                next_cycle[SPAWN_INTERVAL-1] = next_cycle.get(SPAWN_INTERVAL-1, 0) + count
                next_cycle[SPAWN_INTERVAL+START_SHIFT-1] = count
            else:
                next_cycle[age - 1] = count
        by_age = next_cycle
    return sum(by_age.values())


assert evolve(test_data, 80) == 5934
assert evolve(test_data, 256) == 26984457539
print("Part 1:", evolve(data, 80))
print("Part 2:", evolve(data, 256))
