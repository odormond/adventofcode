#! /usr/bin/env python

from itertools import combinations
from math import gcd

import advent_of_code as adv


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = self.vy = self.vz = 0

    def update_speed(self, dv, axis):
        axis = 'v' + axis
        setattr(self, axis, getattr(self, axis) + dv)

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def e_pot(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def e_kin(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def energy(self):
        return self.e_pot() * self.e_kin()

    def __str__(self):
        return f'pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.vx}, y={self.vy}, z={self.vz}>'


def to_positions(text):
    return tuple(
        Moon(*(int(axis.split('=')[1]) for axis in line.strip()[1:-1].split(', ')))
        for line in text.splitlines()
    )


def tick(moons):
    for a, b in combinations(moons, 2):
        for axis in 'xyz':
            pa = getattr(a, axis)
            pb = getattr(b, axis)
            dv = 0
            if pa < pb:
                dv = 1
            elif pa > pb:
                dv = -1
            a.update_speed(dv, axis)
            b.update_speed(-dv, axis)
    for moon in moons:
        moon.update_position()



TEST_1 = "<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>"
test_1 = to_positions(TEST_1)
for step_result in (
    "pos=<x=2, y=-1, z=1>, vel=<x=3, y=-1, z=-1>\npos=<x=3, y=-7, z=-4>, vel=<x=1, y=3, z=3>\npos=<x=1, y=-7, z=5>, vel=<x=-3, y=1, z=-3>\npos=<x=2, y=2, z=0>, vel=<x=-1, y=-3, z=1>",
    "pos=<x=5, y=-3, z=-1>, vel=<x=3, y=-2, z=-2>\npos=<x=1, y=-2, z=2>, vel=<x=-2, y=5, z=6>\npos=<x=1, y=-4, z=-1>, vel=<x=0, y=3, z=-6>\npos=<x=1, y=-4, z=2>, vel=<x=-1, y=-6, z=2>",
    "pos=<x=5, y=-6, z=-1>, vel=<x=0, y=-3, z=0>\npos=<x=0, y=0, z=6>, vel=<x=-1, y=2, z=4>\npos=<x=2, y=1, z=-5>, vel=<x=1, y=5, z=-4>\npos=<x=1, y=-8, z=2>, vel=<x=0, y=-4, z=0>",
    "pos=<x=2, y=-8, z=0>, vel=<x=-3, y=-2, z=1>\npos=<x=2, y=1, z=7>, vel=<x=2, y=1, z=1>\npos=<x=2, y=3, z=-6>, vel=<x=0, y=2, z=-1>\npos=<x=2, y=-9, z=1>, vel=<x=1, y=-1, z=-1>",
    "pos=<x=-1, y=-9, z=2>, vel=<x=-3, y=-1, z=2>\npos=<x=4, y=1, z=5>, vel=<x=2, y=0, z=-2>\npos=<x=2, y=2, z=-4>, vel=<x=0, y=-1, z=2>\npos=<x=3, y=-7, z=-1>, vel=<x=1, y=2, z=-2>",
    "pos=<x=-1, y=-7, z=3>, vel=<x=0, y=2, z=1>\npos=<x=3, y=0, z=0>, vel=<x=-1, y=-1, z=-5>\npos=<x=3, y=-2, z=1>, vel=<x=1, y=-4, z=5>\npos=<x=3, y=-4, z=-2>, vel=<x=0, y=3, z=-1>",
    "pos=<x=2, y=-2, z=1>, vel=<x=3, y=5, z=-2>\npos=<x=1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>\npos=<x=3, y=-7, z=5>, vel=<x=0, y=-5, z=4>\npos=<x=2, y=0, z=0>, vel=<x=-1, y=4, z=2>",
    "pos=<x=5, y=2, z=-2>, vel=<x=3, y=4, z=-3>\npos=<x=2, y=-7, z=-5>, vel=<x=1, y=-3, z=-1>\npos=<x=0, y=-9, z=6>, vel=<x=-3, y=-2, z=1>\npos=<x=1, y=1, z=3>, vel=<x=-1, y=1, z=3>",
    "pos=<x=5, y=3, z=-4>, vel=<x=0, y=1, z=-2>\npos=<x=2, y=-9, z=-3>, vel=<x=0, y=-2, z=2>\npos=<x=0, y=-8, z=4>, vel=<x=0, y=1, z=-2>\npos=<x=1, y=1, z=5>, vel=<x=0, y=0, z=2>",
    "pos=<x=2, y=1, z=-3>, vel=<x=-3, y=-2, z=1>\npos=<x=1, y=-8, z=0>, vel=<x=-1, y=1, z=3>\npos=<x=3, y=-6, z=1>, vel=<x=3, y=2, z=-3>\npos=<x=2, y=0, z=4>, vel=<x=1, y=-1, z=-1>",
):
    tick(test_1)
    assert '\n'.join(str(moon) for moon in test_1) == step_result

assert tuple(moon.energy() for moon in test_1) == (36, 45, 80, 18)


TEST_2 = "<x=-8, y=-10, z=0>\n<x=5, y=5, z=10>\n<x=2, y=-7, z=3>\n<x=9, y=-8, z=-3>"
test_2 = to_positions(TEST_2)
for ten_steps_result in (
    "pos=<x=-9, y=-10, z=1>, vel=<x=-2, y=-2, z=-1>\npos=<x=4, y=10, z=9>, vel=<x=-3, y=7, z=-2>\npos=<x=8, y=-10, z=-3>, vel=<x=5, y=-1, z=-2>\npos=<x=5, y=-10, z=3>, vel=<x=0, y=-4, z=5>",
    "pos=<x=-10, y=3, z=-4>, vel=<x=-5, y=2, z=0>\npos=<x=5, y=-25, z=6>, vel=<x=1, y=1, z=-4>\npos=<x=13, y=1, z=1>, vel=<x=5, y=-2, z=2>\npos=<x=0, y=1, z=7>, vel=<x=-1, y=-1, z=2>",
    "pos=<x=15, y=-6, z=-9>, vel=<x=-5, y=4, z=0>\npos=<x=-4, y=-11, z=3>, vel=<x=-3, y=-10, z=0>\npos=<x=0, y=-1, z=11>, vel=<x=7, y=4, z=3>\npos=<x=-3, y=-2, z=5>, vel=<x=1, y=2, z=-3>",
    "pos=<x=14, y=-12, z=-4>, vel=<x=11, y=3, z=0>\npos=<x=-1, y=18, z=8>, vel=<x=-5, y=2, z=3>\npos=<x=-5, y=-14, z=8>, vel=<x=1, y=-2, z=0>\npos=<x=0, y=-12, z=-2>, vel=<x=-7, y=-3, z=-3>",
    "pos=<x=-23, y=4, z=1>, vel=<x=-7, y=-1, z=2>\npos=<x=20, y=-31, z=13>, vel=<x=5, y=3, z=4>\npos=<x=-4, y=6, z=1>, vel=<x=-1, y=1, z=-3>\npos=<x=15, y=1, z=-5>, vel=<x=3, y=-3, z=-3>",
    "pos=<x=36, y=-10, z=6>, vel=<x=5, y=0, z=3>\npos=<x=-18, y=10, z=9>, vel=<x=-3, y=-7, z=5>\npos=<x=8, y=-12, z=-3>, vel=<x=-2, y=1, z=-7>\npos=<x=-18, y=-8, z=-2>, vel=<x=0, y=6, z=-1>",
    "pos=<x=-33, y=-6, z=5>, vel=<x=-5, y=-4, z=7>\npos=<x=13, y=-9, z=2>, vel=<x=-2, y=11, z=3>\npos=<x=11, y=-8, z=2>, vel=<x=8, y=-6, z=-7>\npos=<x=17, y=3, z=1>, vel=<x=-1, y=-1, z=-3>",
    "pos=<x=30, y=-8, z=3>, vel=<x=3, y=3, z=0>\npos=<x=-2, y=-4, z=0>, vel=<x=4, y=-13, z=2>\npos=<x=-18, y=-7, z=15>, vel=<x=-8, y=2, z=-2>\npos=<x=-2, y=-1, z=-8>, vel=<x=1, y=8, z=0>",
    "pos=<x=-25, y=-1, z=4>, vel=<x=1, y=-3, z=4>\npos=<x=2, y=-9, z=0>, vel=<x=-3, y=13, z=-1>\npos=<x=32, y=-8, z=14>, vel=<x=5, y=-4, z=6>\npos=<x=-1, y=-2, z=-8>, vel=<x=-3, y=-6, z=-9>",
    "pos=<x=8, y=-12, z=-9>, vel=<x=-7, y=3, z=0>\npos=<x=13, y=16, z=-3>, vel=<x=3, y=-11, z=-5>\npos=<x=-29, y=-11, z=-1>, vel=<x=-3, y=7, z=4>\npos=<x=16, y=-13, z=23>, vel=<x=7, y=1, z=1>",
):
    for _ in range(10):
        tick(test_2)
    assert '\n'.join(str(moon) for moon in test_2) == ten_steps_result

assert tuple(moon.energy() for moon in test_2) == (290, 608, 574, 468)


INPUT = adv.input(12, str)
moons = to_positions(INPUT)
for _ in range(1000):
    tick(moons)
print("Part one:", sum(moon.energy() for moon in moons))


def state(moons, axis):
    return tuple((getattr(moon, axis), getattr(moon, 'v'+axis)) for moon in moons)


def find_cycles(moons):
    states = {'x': set(), 'y': set(), 'z': set()}
    cycles = {'x': 0, 'y': 0, 'z': 0}
    while 0 in cycles.values():
        for axis in 'xyz':
            s = state(moons, axis)
            if cycles[axis] == 0 and s in states[axis]:
                cycles[axis] = len(states[axis])
            else:
                states[axis].add(s)
        tick(moons)

    return cycles


def smallest_common_multiple(a, b, *seq):
    scm = 0
    seq = a, b, *seq
    while True:
        a, b, *seq = seq
        scm = a * b // gcd(a, b)
        if not seq:
            break
        seq = scm, *seq
    return scm


assert smallest_common_multiple(*find_cycles(to_positions(TEST_1)).values()) == 2772
assert smallest_common_multiple(*find_cycles(to_positions(TEST_2)).values()) == 4686774924

print("Part two:", smallest_common_multiple(*find_cycles(to_positions(INPUT)).values())) 
