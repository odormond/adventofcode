#! /usr/bin/env python3

import math
import os.path
import advent_of_code as adv

TEST = """
939
7,13,x,x,59,x,31,19
"""


def parse_input(text):
    timestamp, buses = text.strip().splitlines()
    buses = buses.split(',')
    return int(timestamp), [(i, int(bus_id)) for i, bus_id in enumerate(buses) if bus_id != 'x']


def next_bus(earliest, buses):
    departures = sorted(((earliest // bus_id + 1) * bus_id, bus_id) for _, bus_id in buses)
    timestamp, bus_id = departures[0]
    return (timestamp - earliest) * bus_id


assert next_bus(*parse_input(TEST)) == 295

earliest, buses = adv.input(int(os.path.basename(os.path.dirname(__file__))), parse_input)
print("Part 1:", next_bus(earliest, buses))


def special_t(buses):
    t, step = buses.pop(0)
    t = step - t
    while buses:
        phase, cycle = buses.pop(0)
        while (t + phase) % cycle != 0:
            t += step
        step *= cycle
    return t


assert special_t(parse_input(TEST)[1]) == 1068781

print("Part 2:", special_t(buses), time.time() - t0)
