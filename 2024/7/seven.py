#! /usr/bin/env python

from itertools import product

import advent_of_code as aoc

test_data = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

def parse(data):
    return [
        (int(result), [int(v) for v in operand.split()])
        for line in data.splitlines() for result, operand in [line.split(": ")]
    ]


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concat(a, b):
    return int(str(a) + str(b))


def compute(ops, operands):
    ops = list(ops)
    stack = operands[:]
    while ops:
        op = ops.pop(0)
        a, b, *stack = stack
        stack.insert(0, op(a, b))
    return stack[0]


def solver(tests, operators):
    total = 0
    for result, operands in tests:
        for ops in product(operators, repeat=(len(operands) - 1)):
            if compute(ops, operands) == result:
                total += result
                break
    return total


def part1(data):
    tests = parse(data)
    return solver(tests, (add, mul))


assert (result := part1(test_data)) == 3749, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    tests = parse(data)
    return solver(tests, (add, mul, concat))


assert (result := part2(test_data)) == 11387, f"{result=}"
print("Part 2:", part2(aoc.input()))
