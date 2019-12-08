#! /usr/bin/env python

import advent_of_code as adv

TEST_MAP = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L"


class System:
    def __init__(self):
        self.bodies = {}

    @classmethod
    def from_orbit_map(cls, text):
        system = System()
        for line in text.splitlines():
            parent, body = line.split(')')
            system.add_body(body, parent)
        assert [b.name for b in system.bodies.values() if b.parent is None] == ['COM'], "Non unique Center Of Mass"
        return system

    def add_body(self, name, parent):
        parent = self.bodies.setdefault(parent, Body(parent, None))
        body = self.bodies.setdefault(name, Body(name, parent))
        body.parent = parent

    def orbits(self, body):
        body = self.bodies[body]
        parents = []
        while body.parent is not None:
            body = body.parent
            parents.append(body)
        return parents

    def total_orbits(self):
        return sum(len(self.orbits(b)) for b in self.bodies)

    def transfers(self, src, dest):
        down = set(self.orbits(src))
        up = set(self.orbits(dest))
        common = down.intersection(up)
        down.difference_update(common)
        up.difference_update(common)
        return len(down) + len(up)


class Body:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent


test_system = System.from_orbit_map(TEST_MAP)
assert len(test_system.orbits('D')) == 3
assert len(test_system.orbits('L')) == 7
assert len(test_system.orbits('COM')) == 0
assert test_system.total_orbits() == 42

system = adv.input(6, System.from_orbit_map)

print("Part one:", system.total_orbits())


TEST_TRANSFER = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"
test_system = System.from_orbit_map(TEST_TRANSFER)
assert test_system.transfers('YOU', 'SAN') == 4


print("Part two:", system.transfers('YOU', 'SAN'))
