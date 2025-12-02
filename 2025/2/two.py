#! /usr/bin/env python

from math import floor

import advent_of_code as aoc

test_data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

def parse(data):
    id_ranges = []
    for product_range in data.split(","):
        low, hi = product_range.split("-")
        id_ranges.append((int(low), int(hi)))
    return id_ranges


def part1(data):
    invalid_total = 0
    for low, hi in parse(data):
        low_str = str(low)
        hi_str = str(hi)
        start = int(low_str[:len(low_str)//2]) if len(low_str) > 1 else low
        end = int(hi_str[:floor(len(hi_str)/2 + 0.5)])
        for i in range(start, end+1):
            i = int(str(i)*2)
            if i < low:
                continue
            if low <= i <= hi:
                invalid_total += i
            elif i > hi:
                break
    return invalid_total


assert (result := part1(test_data)) == 1227775554, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    invalid_total = 0
    for low, hi in parse(data):
        for i in range(low, hi+1):
            i = str(i)
            l = len(i)
            for s in range(1, l//2 + 1):
                if l % s:
                    continue
                if i[:s] * (l // s) == i:
                    invalid_total += int(i)
                    break
    return invalid_total


assert (result := part2(test_data)) == 4174379265, f"{result=}"
print("Part 2:", part2(aoc.input()))
