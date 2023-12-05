#! /usr/bin/env python

from itertools import combinations
from math import inf

import advent_of_code as adv

test_data = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


class CompactMap:
    def __init__(self):
        self.ranges = []

    def add(self, dest, src, length):
        self.ranges = sorted(self.ranges + [(src, dest, length)])

    def __getitem__(self, key):
        for src, dest, length in self.ranges:
            if src <= key < src + length:
                return dest + (key - src)
        return key


def parse_seeds(data):
    return [int(v) for v in data.split(': ')[1].split()]


def parse_map(data):
    result = CompactMap()
    for line in data.splitlines()[1:]:
        result.add(*[int(v) for v in line.split()])
    return result


def parse(data):
    blocks = data.split('\n\n')
    return (
        parse_seeds(blocks[0]),
        parse_map(blocks[1]),  # seed_to_soil
        parse_map(blocks[2]),  # soil_to_fertilizer
        parse_map(blocks[3]),  # fertilizer_to_water
        parse_map(blocks[4]),  # water_to_light
        parse_map(blocks[5]),  # light_to_temperature
        parse_map(blocks[6]),  # temperature_to_humidity
        parse_map(blocks[7]),  # humidity_to_location
    )


def part1(data):
    seeds, *maps = parse(data)
    closest_location = inf
    for key in seeds:
        for mapping in maps:
            key = mapping[key]
        closest_location = min(closest_location, key)
    return closest_location


assert (result := part1(test_data)) == 35, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    seeds, *maps = parse(data)
    ranges = list(zip(seeds[::2], seeds[1::2]))
    for m in maps:
        next_ranges = []
        for seed, count in ranges:
            for src, dest, length in m.ranges:
                if seed + count - 1 < src:
                    # maps on itself
                    next_ranges.append((seed, count))
                    break  # all the other ranges are above this one
                elif seed < src:
                    # overlaps before the start
                    left_length = src - seed
                    next_ranges.append((seed, left_length))  # this part maps on itself
                    if count - left_length <= length:
                        # all the rest maps to destination
                        next_ranges.append((dest, count - left_length))
                        break
                    else:
                        # only the midle part maps to this destination
                        next_ranges.append((dest, length))
                        seed, count = src + length, count - left_length - length
                elif seed <= src + length:
                    # overlaps after the start
                    if seed + count < src + length:
                        # maps entirely to destination
                        next_ranges.append((dest + seed - src, count))
                        break
                    else:
                        # only the beginning maps
                        next_ranges.append((dest + seed - src, length - (seed - src)))
                        seed, count = src + length, count - (length - (seed - src))
            else:
                # maps on itself after all the ranges
                next_ranges.append((seed, count))
        ranges = next_ranges
    return min(l for l, _ in ranges)


assert (result := part2(test_data)) == 46, f"{result=}"
print("Part 2:", part2(adv.input()))
