#! /usr/bin/env python3

from advent import Inputs

frequencies_hops = [int(h) for h in Inputs(2018).get(1).iter_lines(decode_unicode=True)]

print("Part one:", sum(frequencies_hops))

seen = set()
freq = 0
while True:
    for f in frequencies_hops:
        freq += f
        if freq in seen:
            print("Part two:", freq)
            raise SystemExit(0)
        seen.add(freq)
