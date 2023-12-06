#! /usr/bin/env python

import math
import re

import advent_of_code as adv

test_data = """\
Time:      7  15   30
Distance:  9  40  200
"""

def parse(data):
    times, distances = data.splitlines()
    times = map(int, re.findall(r'\d+', times))
    distances = map(int, re.findall(r'\d+', distances))
    return zip(times, distances)


def part1(data):
    # d = (t - v) * v = t * v - v**2
    # v**2 - t * v + d = 0
    # v = (t +- (t**2 - 4 * d)**0.5) / 2
    combinations = 1
    for time, distance in parse(data):
        delta = (time**2 - 4*distance)**0.5
        charge1 = (time - delta) / 2
        charge2 = (time + delta) / 2
        if int(charge1) == charge1:
            charge1 = int(charge1 + 1)
        else:
            charge1 = math.ceil(charge1)
        if int(charge2) == charge2:
            charge2 = int(charge2 - 1)
        else:
            charge2 = math.floor(charge2)
        combinations *= (charge2 - charge1 + 1)
    return combinations


assert (result := part1(test_data)) == 288, f"{result=}"
print("Part 1:", part1(adv.input()))


def parse(data):
    times, distances = data.splitlines()
    _, times = times.split(':')
    _, distances = distances.split(':')
    time = int(times.replace(' ', ''))
    distance = int(distances.replace(' ', ''))
    return [(time, distance)]

def part2(data):
    return part1(data)


assert (result := part2(test_data)) == 71503, f"{result=}"
print("Part 2:", part2(adv.input()))
