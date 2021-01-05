#! /usr/bin/env python3

from math import log
import os.path
import advent_of_code as adv


def loop(size, subject):
    return subject ** size % 20201227


def find_size(pub_key):
    i = 0
    while i < 1000000000:  # Random guard value
        if i % 1000 == 0:
            print(f'\r{i}', end='')
        size = log(pub_key + 20201227 * i) / log(7)
        if int(size) == size:
            return int(size)
        i += 1
    else:
        assert False, "Hit guard"


def loop(size, subject):
    value = 1
    for _ in range(size):
        value = (value * subject) % 20201227
    return value


def find_size(key):
    size = 0
    value = 1
    while value != key:
        value = (value * 7) % 20201227
        size += 1
    return size


def break_encryption(pub1, pub2):
    return loop(find_size(pub1), pub2)


assert find_size(5764801) == 8
assert find_size(17807724) == 11
assert loop(11, 5764801) == loop(8, 17807724) == 14897079

card, door = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_int)
card_size = find_size(card)
print("Part 1:", loop(card_size, door))
