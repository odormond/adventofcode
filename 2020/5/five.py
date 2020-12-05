#! /usr/bin/env python3

import os.path
import advent_of_code as adv


def binary_split(splits, low, hi):
    for split in splits:
        if split in "FL":
            hi = low + (hi - low) // 2
        else:
            low = low + (hi - low) // 2 + 1
    assert low == hi
    return low


def pass_to_seat_id(boarding_pass):
    row = binary_split(boarding_pass[:7], 0, 127)
    column = binary_split(boarding_pass[7:], 0, 7)
    return row * 8 + column


for p, s in (("FBFBBFFRLR", 357), ("BFFFBBFRRR", 567), ("FFFBBBFRRR", 119), ("BBFFBBFRLL", 820)):
    assert pass_to_seat_id(p) == s


data = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_str)

seat_ids = sorted(pass_to_seat_id(boarding_pass) for boarding_pass in data)
print("Part 1:", max(seat_ids))

for i in range(len(seat_ids) - 1):
    if seat_ids[i] + 2 == seat_ids[i + 1]:
        print("Part 2:", seat_ids[i] + 1)
