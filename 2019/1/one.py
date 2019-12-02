#! /usr/bin/env python

import advent_of_code as adv


def fuel(module):
    return max(module // 3 - 2, 0)

assert fuel(1969) == 654
assert fuel(100756) == 33583

modules = adv.input(1, adv.to_list_of_int)

print("Part 1:", sum(map(fuel, modules)))


def total_fuel(module):
    total_fuel = 0
    f = fuel(module)
    while f:
        total_fuel += f
        f = fuel(f)
    return total_fuel

assert total_fuel(14) == 2
assert total_fuel(1969) == 966
assert total_fuel(100756) == 50346

print("Part 2:", sum(map(total_fuel, modules)))
