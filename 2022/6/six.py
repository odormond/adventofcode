#! /usr/bin/env python

import advent_of_code as adv

test_data = (
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 4),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 4),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 4),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 4),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 4),
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19, 14),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23, 14),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23, 14),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29, 14),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26, 14),
)


def find_start_marker(data, size):
    window = []
    for i, c in enumerate(data):
        window = window[-size+1:] + [c]
        if len(set(window)) == size:
            return i + 1


for test, expected, size in test_data:
    found = find_start_marker(test, size)
    assert found == expected, f"Wrong marker location {found} in {test}; expected {expected}"

print("Part 1:", find_start_marker(adv.input(), 4))
print("Part 2:", find_start_marker(adv.input(), 14))
