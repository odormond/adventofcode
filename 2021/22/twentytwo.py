#! /usr/bin/env python

from math import inf
from pathlib import Path
import advent_of_code as adv


def parse(text):
    steps = []
    for step in text.strip().splitlines():
        state, cube = step.split()
        state = state == 'on'
        bounds = tuple(
            zip(
                *[
                    [int(a) + i for i, a in enumerate(axis[2:].split('..'))]
                    for axis in cube.split(',')
                ]
            )
        )
        steps.append((state, bounds))
    return steps


test_steps = parse(Path(__file__).with_name('test_data').read_text())
test2_steps = parse(Path(__file__).with_name('test2_data').read_text())
test3_steps = parse(Path(__file__).with_name('test3_data').read_text())
pb_steps = adv.input(Path(__file__).parent.name, parse)


def overlap(a, b):
    (lxa, lya, lza), (hxa, hya, hza) = a
    (lxb, lyb, lzb), (hxb, hyb, hzb) = b
    if lxa < hxb and hxa > lxb:
        lxo = max(lxa, lxb)
        hxo = min(hxa, hxb)
        if lya < hyb and hya > lyb:
            lyo = max(lya, lyb)
            hyo = min(hya, hyb)
            if lza < hzb and hza > lzb:
                lzo = max(lza, lzb)
                hzo = min(hza, hzb)
                return (lxo, lyo, lzo), (hxo, hyo, hzo)
    return None


def disjoin(region, cover):
    if cover is None:  # No intersection, region is disjoin from cover
        return region
    (rlx, rly, rlz), (rhx, rhy, rhz) = region
    (clx, cly, clz), (chx, chy, chz) = cover
    # yield up to 6 sub regions
    if rlx < clx:
        yield (rlx, rly, rlz), (clx, rhy, rhz)  # along x: rc.
    if chx < rhx:
        yield (chx, rly, rlz), (rhx, rhy, rhz)  # along x: .cr
    if rly < cly:
        yield (clx, rly, rlz), (chx, cly, rhz)  # along y: rc.
    if chy < rhy:
        yield (clx, chy, rlz), (chx, rhy, rhz)  # along y: .cr
    if rlz < clz:
        yield (clx, cly, rlz), (chx, chy, clz)  # along z: rc.
    if chz < rhz:
        yield (clx, cly, chz), (chx, chy, rhz)  # along z: .cr
    # If nothing before, full overlap, nothing can be separated from cover


class Reactor:
    def __init__(self):
        self.regions = {}

    def set(self, bounds, new_value):
        self.regions, regions = {}, self.regions
        for region, old_value in regions.items():
            cover = overlap(region, bounds)
            if cover is None:
                self.regions[region] = old_value
                continue
            for region in disjoin(region, cover):
                self.regions[region] = old_value
        if new_value:
            self.regions[bounds] = new_value

    def reboot(self, steps):
        for value, bounds in steps:
            self.set(bounds, value)
        return self

    def clip(self, bounds):
        (lx, ly, lz), (hx, hy, hz) = bounds
        self.set(((-inf, -inf, -inf), (lx, inf, inf)), 0)
        self.set(((hx, -inf, -inf), (inf, inf, inf)), 0)
        self.set(((lx, -inf, -inf), (hx, ly, inf)), 0)
        self.set(((lx, hy, -inf), (hx, inf, inf)), 0)
        self.set(((lx, ly, -inf), (hx, hy, lz)), 0)
        self.set(((lx, ly, hz), (hx, hy, inf)), 0)
        return self

    @property
    def actives(self):
        total = 0
        for region, value in self.regions.items():
            if value is False:
                continue
            (lx, ly, lz), (hx, hy, hz) = region
            total += (hx - lx) * (hy - ly) * (hz - lz)
        return total


test_reactor = Reactor()
assert test_reactor.reboot(test_steps).clip(((-50, -50, -50), (51, 51, 51))).actives == 39
test2_reactor = Reactor()
assert test2_reactor.reboot(test2_steps).clip(((-50, -50, -50), (51, 51, 51))).actives == 590784
pb_reactor = Reactor()
print("Part 1:", pb_reactor.reboot(pb_steps).clip(((-50, -50, -50), (51, 51, 51))).actives)

test3_reactor = Reactor()
assert test3_reactor.reboot(test3_steps).clip(((-50, -50, -50), (51, 51, 51))).actives == 474140
test3_reactor = Reactor()
assert test3_reactor.reboot(test3_steps).actives == 2758514936282235
pb_reactor = Reactor()
print("Part 2:", pb_reactor.reboot(pb_steps).actives)
