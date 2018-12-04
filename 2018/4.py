#! /usr/bin/env python3

import operator
import re

from advent import Inputs


RECORD_RE = re.compile(r'\[\d{4}-(.*) \d\d:(\d\d)\] (?:Guard #(\d+) begins shift|falls (asleep)|wakes (up))')


def split_record(r):
    match = RECORD_RE.match(r)
    day, minute, guard, asleep, up = match.groups()
    return day, int(minute), guard or asleep or up


journal = sorted(split_record(r) for r in Inputs(2018).get(4).iter_lines(decode_unicode=True))


guards_sleeps = {}
start_sleep = None
for day, minute, action in journal:
    if action == 'asleep':
        start_sleep = minute
    else:  # woke up or new shift
        if start_sleep is not None:
            hour[start_sleep:minute] = ['#'] * (minute - start_sleep)
            start_sleep = None
        if action != 'up':  # new shift
            hour = ['.'] * 60
            guards_sleeps.setdefault(int(action), []).append((day, hour))


guards = []

for guard, sleeps in guards_sleeps.items():
    total = 0
    for day, hour in sleeps:
        total += ''.join(hour).count('#')
    guards.append((total, guard))

guards = sorted(guards)
total, guard = guards[-1]  # sleepier


def best_minute(sleeps):
    minutes = [0] * 60
    for day, hour in sleeps:
        for minute, sleep in enumerate(hour):
            if sleep == '#':
                minutes[minute] += 1

    return minutes.index(max(minutes)), max(minutes)


minute, count = best_minute(guards_sleeps[guard])
print("Part one:", guard * minute)


guards = sorted((best_minute(sleeps) + (guard,) for guard, sleeps in guards_sleeps.items()),
                key=operator.itemgetter(1))
minute, count, guard = guards[-1]
print("Part two:", guard * minute)
