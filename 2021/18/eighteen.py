#! /usr/bin/env python

from functools import reduce
from itertools import permutations
from pathlib import Path
import advent_of_code as adv


def flatten(number, path=()):
    if type(number) == int:
        return [(number, path)]
    a, b = number
    return flatten(a, path + (0,)) + flatten(b, path + (1,))


def reshape(flat):
    number = flat[:]
    while number[0][1] != ():
        for i, ((left, path_l), (right, path_r)) in enumerate(zip(number[:-1], number[1:])):
            if path_l[:-1] == path_r[:-1]:
                number[i:i+2] = [([left, right], path_l[:-1])]
                break
    return number[0][0]


def reduce_once(number):
    flat = flatten(number)
    # Explode
    for i, (a, path) in enumerate(flat):
        if len(path) == 5:  # In a pair nested 4 times
            b = flat[i+1][0]
            flat[i:i+2] = [(0, path[:-1])]
            if i > 0:  # We have at least one element left
                value, path = flat[i - 1]
                flat[i - 1] = value + a, path
            if i + 1 < len(flat):  # We have a least one element right
                value, path = flat[i + 1]
                flat[i + 1] = b + value, path
            return reshape(flat)
    # Split
    for i, (value, path) in enumerate(flat):
        if value >= 10:
            flat[i:i+1] = [(value // 2, path + (0,)), (value - value // 2, path + (1,))]
            return reshape(flat)
    return number


def add(a, b):
    number = [a, b]
    while (reduced := reduce_once(number)) != number:
        number = reduced
    return number


def magnitude(number):
    if type(number) == int:
        return number
    a, b = number
    return 3 * magnitude(a) + 2 * magnitude(b)


def to_list_of_snailfish(text):
    return [eval(line) for line in text.splitlines()]


assert reduce_once([[[[[9, 8], 1], 2], 3], 4]) == [[[[0, 9], 2], 3], 4]
assert reduce_once([7, [6, [5, [4, [3, 2]]]]]) == [7, [6, [5, [7, 0]]]]
assert reduce_once([[6, [5, [4, [3, 2]]]], 1]) == [[6, [5, [7, 0]]], 3]
assert reduce_once([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]) == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
assert reduce_once([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]) == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]

assert add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

assert reduce(add, [[i, i] for i in range(1, 7)]) == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]
assert reduce(add, to_list_of_snailfish(Path(__file__).with_name('test_data').read_text())) == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
assert reduce(add, (test_data := to_list_of_snailfish(Path(__file__).with_name('test_data_2').read_text()))) == [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]

assert magnitude([[9, 1], [1, 9]]) == 129
assert magnitude([[1, 2], [[3, 4], 5]]) == 143
assert magnitude([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == 1384
assert magnitude([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == 445
assert magnitude([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]) == 791
assert magnitude([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]) == 1137
assert magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]) == 3488
assert magnitude([[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]) == 4140

homework = adv.input(Path(__file__).parent.name, to_list_of_snailfish)

print("Part 1:", magnitude(reduce(add, homework)))


def largest_pair_addition_magnitude(seq):
    return max(magnitude(add(a, b)) for a, b in permutations(seq, 2))


assert largest_pair_addition_magnitude(test_data) == 3993

print("Part 2:", largest_pair_addition_magnitude(homework))
