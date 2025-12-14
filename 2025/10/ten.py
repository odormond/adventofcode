#! /usr/bin/env python

from functools import cache, reduce
from itertools import chain, combinations
from math import inf
from multiprocessing import Pool
from operator import xor

import advent_of_code as aoc

test_data = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def parse(data):
    for line in data.splitlines():
        indicators, *buttons, joltages = line.split()
        indicators = sum(2**i for i, l in enumerate(indicators[1:-1]) if l == "#")
        buttons = [{int(v) for v in button[1:-1].split(",")} for button in buttons]
        joltages = tuple(int(v) for v in joltages[1:-1].split(","))
        #print(line)
        yield (indicators, buttons, joltages)


def flips(machine):
    target, buttons, _ = machine
    buttons = [sum(2**b for b in button) for button in buttons]
    states = dict(
        sorted(
            (
                (reduce(xor, presses, 0), len(presses))
                for presses in chain.from_iterable(
                    combinations(buttons, r+1) for r in range(len(buttons))
                )
            ),
            reverse=True,
        )
    )
    return states.get(target)


def part1(data):
    with Pool() as pool:
        return sum(pool.map(flips, parse(data)))


def presses(machine):
    _, buttons, target = machine
    zero = tuple([0] * len(target))

    buttons = [tuple(int(i in button) for i in range(len(target))) for button in buttons]
    states = dict(
        sorted(
            (
                (tuple(sum(p) for p in zip(zero, *presses)), len(presses))
                for presses in chain.from_iterable(
                    combinations(buttons, r) for r in range(len(buttons)+1)
                )
            ),
            reverse=True,
        )
    )

    @cache
    def recurse(target):
        if target == zero:
            return 0
        result = inf
        for state, presses in states.items():
            if all(s <= t and s % 2 == t % 2 for s, t in zip(state, target)):
                new_target = tuple((t - s) // 2 for s, t in zip(state, target))
                result = min(result, presses + 2 * recurse(new_target))
        return result

    result = recurse(target)
    return result


def part2(data):
    with Pool() as pool:
        return sum(pool.map(presses, parse(data)))


if __name__ == "__main__":
    assert (result := part1(test_data)) == 7, f"{result=}"
    print("Part 1:", part1(aoc.input()))

    assert (result := part2(test_data)) == 33, f"{result=}"
    print("Part 2:", part2(aoc.input()))
