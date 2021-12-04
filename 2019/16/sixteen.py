#! /usr/bin/env python

from itertools import zip_longest
from time import time

import advent_of_code as adv

def digits(text):
    return [int(c) for c in text.strip()]


BASE_PATTERN = [0, 1, 0, -1]

def last_digit(num):
    return num % 10 if num >= 0 else (-num % 10)


def pattern(pos, l):
    skip = pos + 1
    for _ in range(l):
        for p in BASE_PATTERN:
            for i in range(pos+1):
                if skip:
                    skip -= 1
                    continue
                yield p


def alternate(repeat, length):
    step = 4 * repeat
    for r in range(repeat):
        for plus, minus in zip_longest(range(repeat-1 + r, length, step), range(2+3*(repeat-1) + r, length, step)):
            if plus is not None:
                yield plus, 1
            if minus is not None:
                yield minus, -1
        

def phase(signal):
    l = len(signal)
    return [
        last_digit(sum(signal[index] * weight for index, weight in alternate(i+1, l)))
        for i in range(l)
    ]
            
    return [
        last_digit(sum(s*p for s, p in zip(signal[i:], pattern(i, l)) if p))
        for i in range(l)
    ]


signal = digits('12345678')
for output in ('48226158', '34040438', '03415518', '01029498'):
    signal = phase(signal)
    assert signal == digits(output), f"{signal} != {digits(output)}"


def decode(signal):
    for _ in range(100):
        signal = phase(signal)
    return signal


for signal, check in (
    ('80871224585914546619083218645595', '24176176'),
    ('19617804207202209144916044189917', '73745418'),
    ('69317163492948606335995924319873', '52432133'),
):
    assert decode(digits(signal))[:8] == digits(check)


INPUT = adv.input(16, lambda x: x.strip())
print("Part one:", ''.join(map(str, decode(digits(INPUT))[:8])))

def speed_test():
    for repeat in range(1, 5):
        t0 = time()
        decode(digits(INPUT * repeat))
        print(repeat, time()-t0)

import cProfile as profile
profile.runctx("speed_test()", globals(), locals())

raise SystemExit(0)

REPEAT = 10000
for signal, check in (
    ('03036732577212944063491565474664', '84462026'),
    ('02935109699940807407585447034323', '78725270'),
    ('03081770884921959731165446850517', '53553731'),
):
    offset = int(signal[:7])
    assert decode(digits(signal * REPEAT))[offset:offset+8] == digits(check)

offset = int(INPUT[:7])
print("Part two:", ''.join(map(str, decode(digits(INPUT * REPEAT))[offset:offset+8])))
