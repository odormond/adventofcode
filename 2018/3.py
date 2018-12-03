#! /usr/bin/env python3

import operator
import re

from advent import Inputs


class Claim:
    CLAIM_RE = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

    def __init__(self, claim):
        match = self.CLAIM_RE.match(claim)
        assert match is not None, f"{claim!r} doesn't match the expected format"
        self.num, self.left, self.top, self.width, self.height = tuple(int(g) for g in match.groups())
        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.overlaps = set()

    def places(self):
        for y in range(self.top, self.bottom):
            for x in range(self.left, self.right):
                yield x, y

    def __str__(self):
        return f'#{self.num} @ {self.left},{self.top}: {self.width}x{self.height}'


class Fabric:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fabric = [[] for i in range(width * height)]
        self.overlaps = set()

    def claim(self, claim):
        for x, y in claim.places():
            p = y * self.width + x
            if len(self.fabric[p]) > 0:
                self.overlaps.add(p)
                claim.overlaps.update(self.fabric[p])
                for o in self.fabric[p]:
                    o.overlaps.add(claim)
            self.fabric[p].append(claim)


claims = [Claim(c) for c in Inputs(2018).get(3).iter_lines(decode_unicode=True)]

fabric = Fabric(max(c.right for c in claims), max(c.bottom for c in claims))

for c in claims:
    fabric.claim(c)

print("Part one:", len(fabric.overlaps))


print("Part two:", *[str(c) for c in claims if not c.overlaps])
