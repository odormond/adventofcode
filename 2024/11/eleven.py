#! /usr/bin/env python

from collections import Counter
from functools import cache

import advent_of_code as aoc

test_data = "125 17"

def parse(data):
    return [int(stone) for stone in data.strip().split()]


def step(stones):
    new_state = []
    for stone in stones:
        if stone == 0:
            new_state.append(1)
        elif (l := len(s := str(stone))) % 2 == 0:
            new_state.append(int(s[:l//2]))
            new_state.append(int(s[l//2:]))
        else:
            new_state.append(stone * 2024)
    return new_state


def part1(data):
    stones = parse(data)
    for _ in range(25):
        stones = step(stones)
    return len(stones)


assert (result := part1(test_data)) == 55312, f"{result=}"
print("Part 1:", (result1 := part1(aoc.input())))


"""
70949 6183 4 3825336 613971 0 15 182

0
1
2024
20 24
2 0 2 4

2
4048
40 48
4 0 4 8

3
6072
60 72
6 0 7 2

4
8096
80 96
8 0 9 6

5
10120
20482880
2048 2880
20 48 28 80
2 0 4 8 2 8 8 0

6
24579456
2457 9456
24 57 94 56
2 4 5 7 9 4 5 6

7
14168
28676032
2867 6032
28 67 60 32
2 8 6 7 6 0 3 2

8
16192             <-+
32772608            |
3277 2608           |
32 77 26 8          |
3 2 7 7 2 6 16192 --+

9
18216
36869184
3686 9184
36 86 91 84
3 6 8 6 9 1 8 4
"""


def step2(stones, remaining_steps):
    new_stones = []
    for stone in stones:
        s = str(stone)
        l = len(s)
        if isinstance(stone, tuple):
            new_stones.append(stone)
        elif l == 1 and stone == 0:
            new_stones.append(1)
        elif l == 1:
            new_stones.append((stone, remaining_steps))
        elif l % 2 == 0:
            new_stones.append(int(s[:l//2]))
            new_stones.append(int(s[l//2:]))
        else:
            new_stones.append(stone * 2024)
    return new_stones


@cache
def part2(data, steps):
    stones = parse(data)
    for i in range(steps):
        stones = step2(stones, steps - i - 1)
        if all(isinstance(s, tuple) for s in stones):
            break
    counts = Counter(stones)
    total = 0
    for item, times in counts.items():
        if isinstance(item, int):
            total += times
            continue
        value, remaining_steps = item
        total += part2(str(value * 2024), remaining_steps) * times
    return total

print("Part 2:", part2(aoc.input(), 75))
