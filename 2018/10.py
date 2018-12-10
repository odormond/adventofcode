#! /usr/bin/env python3

import re

from advent import Inputs


class Star:
    LINE_RE = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')

    def __init__(self, line):
        self.x, self.y, self.vx, self.vy = (int(g) for g in self.LINE_RE.match(line).groups())

    def draw(self, left, top):
        return f'\033[{self.y-top};{self.x-left}H#'

    def tick(self):
        self.x += self.vx
        self.y += self.vy


stars = [Star(line.strip()) for line in Inputs(2018).get(10).iter_lines(decode_unicode=True)]


def rectangle(stars):
    left = min(s.x for s in stars)
    width = max(s.x for s in stars) - left
    top = min(s.y for s in stars)
    height = max(s.y for s in stars) - top
    return left, top, width, height


area = None
last_sky = 'N/A'
t = 0
while True:
    left, top, width, height = rectangle(stars)
    if area is not None and area < width * height:
        print('\033[2J' + last_sky, end=f'\033[{height};1H')
        print("Part one displayed above")
        print("Part two:", t-1, "seconds")
        break
    last_sky = ''.join(s.draw(left, top) for s in stars)
    area = width * height
    t += 1
    for s in stars:
        s.tick()
