#! /usr/bin/env python3

import os.path
import re

import advent_of_code as adv

POL_PASS_RE = re.compile(r"^(?P<low>\d+)-(?P<hi>\d+) (?P<char>.): (?P<password>.+)")

passwords = adv.input(int(os.path.basename(os.path.dirname(__file__))), lambda d: d.splitlines())

sled_rental_valid_cnt = toboggan_valid_cnt = 0
for line in passwords:
    assert line[-1] != "\n"
    low, hi, char, password = POL_PASS_RE.match(line).groups()
    low, hi = int(low), int(hi)
    if low <= password.count(char) <= hi:
        sled_rental_valid_cnt += 1
    if (password[low - 1] == char or password[hi - 1] == char) and password[low - 1] != password[
        hi - 1
    ]:
        toboggan_valid_cnt += 1

print("Part 1:", sled_rental_valid_cnt)
print("Part 2:", toboggan_valid_cnt)
