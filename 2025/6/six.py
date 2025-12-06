#! /usr/bin/env python

import advent_of_code as aoc

test_data = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   + 
"""

def mul(numbers):
    result = 1
    for n in numbers:
        result *= n
    return result


def part1(data):
    lines = data.splitlines()
    values = [
        [int(n) for n in line.strip().split()]
        for line in lines[:-1]
    ]
    operators = lines[-1].strip().split()
    total = 0
    for op, numbers in zip(operators, zip(*values)):
        total += {"+": sum, "*": mul}[op](numbers)
    return total


assert (result := part1(test_data)) == 4277556, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    *numbers, operators = data.splitlines()
    values = []
    group = []
    for chars in zip(*numbers):
        line = ''.join(chars).strip()
        if not line:
            values.append(group)
            group = []
        else:
            group.append(int(line))
    values.append(group)
    operators = operators.strip().split()
    total = 0
    for op, numbers in zip(operators, values):
        total += {"+": sum, "*": mul}[op](numbers)
    return total


assert (result := part2(test_data)) == 3263827, f"{result=}"
print("Part 2:", part2(aoc.input()))
