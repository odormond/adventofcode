#! /usr/bin/env python3

from itertools import chain
import os.path
import advent_of_code as adv


def to_list_of_anyone_answers(text):
    return [set(chain.from_iterable(group.splitlines())) for group in text.strip().split("\n\n")]


TEST = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""

assert sum(map(len, to_list_of_anyone_answers(TEST))) == 11

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), to_list_of_anyone_answers)
print("Part 1:", sum(map(len, data)))


def to_list_of_everyone_answers(text):
    answers = []
    for group in map(str.split, text.strip().split("\n\n")):
        common = set(group.pop())
        while group:
            common.intersection_update(group.pop())
        answers.append(common)
    return answers


assert sum(map(len, to_list_of_everyone_answers(TEST))) == 6

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), to_list_of_everyone_answers)
print("Part 2:", sum(map(len, data)))
