#! /usr/bin/env python

import math
from pathlib import Path
import advent_of_code as adv

test_data = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
data = adv.input(Path(__file__).parent.name, adv.to_list_of_int)


def best_alignment_fuel(positions, cost_fn):
    low, hi = min(positions), max(positions)
    min_fuel = math.inf
    min_target = None
    for target in range(low, hi+1):
        fuel = sum(cost_fn(target - crab) for crab in positions)
        if fuel < min_fuel:
            min_fuel = fuel
            min_target = target
    return int(min_fuel)


def linear_cost(move):
    return abs(move)


def quadratic_cost(move):
    return abs(move) * (abs(move) + 1) / 2


assert best_alignment_fuel(test_data, linear_cost) == 37
print("Part 1:", best_alignment_fuel(data, linear_cost))

assert best_alignment_fuel(test_data, quadratic_cost) == 168
print("Part 2:", best_alignment_fuel(data, quadratic_cost))
