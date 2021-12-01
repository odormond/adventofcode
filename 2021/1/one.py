#! /usr/bin/env python

from pathlib import Path
import advent_of_code as adv

test_data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

def increments(data):
    count = 0
    last = data[0]
    for measure in data[1:]:
        if measure > last:
            count += 1
        last = measure
    return count

assert increments(test_data) == 7

def window_increments(data):
    count = 0
    for i in range(len(data)-3):
        if sum(data[i:i+3]) < sum(data[i+1:i+4]):
            count += 1
    return count

assert window_increments(test_data) == 5

data = adv.input(Path(__file__).parent.name, adv.to_list_of_int)

print("Part 1:", increments(data))
print("Part 2:", window_increments(data))

