#! /usr/bin/env python

from collections import defaultdict
from itertools import chain, product, combinations
from math import ceil
from random import choice
import re

import advent_of_code as adv

test_data = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""

BLUEPRINT_RE = re.compile(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')
DEADLINE = 24


def parse(data):
    blueprints = {}
    for line in data.splitlines():
        match = BLUEPRINT_RE.match(line)
        blueprint, *costs = match.groups()
        blueprints[int(blueprint)] = tuple(int(c) for c in costs)
    return blueprints


class PriorityQueue:
    def __init__(self):
        self.queue = defaultdict(set)
        self.priorities = []

    def push(self, priority, value):
        self.queue[priority].add(value)
        self.priorities = sorted(self.queue, reverse=True)

    def pop(self):
        p = self.priorities[0]
        top = self.queue[p]
        value = top.pop()
        if not top:
            del self.queue[p], self.priorities[0]
        return value

    def __bool__(self):
        return bool(self.priorities)


def concurential(t, geodes, geode_bots, min_geodes):
    # If we were to produce a new geode bot every minute from now but still cannot produce
    # more than the guaranteed min number of geodes from other states then there is no point
    # in progressing this state.
    t_left = DEADLINE - t
    return t_left > 0 and (t_left * (t_left + 1) // 2 + geodes + geode_bots * t_left >= min_geodes)


def crack_geodes(ore_bot_ores, clay_bot_ores, obsidian_bot_ores, obsidian_bot_clays, geode_bot_ores, geode_bot_obsidians):
    # If we have as much as max_FOO_bots we'll produce in a minute enough resource to produce
    # the bot that needs them the most so over-production would be useless.
    max_ore_bots = max(ore_bot_ores, clay_bot_ores, obsidian_bot_ores, geode_bot_ores)
    max_clay_bots = obsidian_bot_clays
    max_obsidian_bots = geode_bot_obsidians
    min_geodes = 0
    state = 0, 0, 0, 0, 0, 1, 0, 0, 0
    queue = PriorityQueue()
    queue.push(0, state)
    while queue:
        t, *state = queue.pop()
        ores, clays, obsidians, geodes, ore_bots, clay_bots, obsidian_bots, geode_bots = state
        if not concurential(t, geodes, geode_bots,  min_geodes):
            continue
        # Keep track of the guaranteed minimum number of geodes that can be produces from this state.
        min_geodes = max(min_geodes, geodes + geode_bots * (DEADLINE - t))
        # Geode bots production is possible only if we have obsidian bots to produce obsidian
        if obsidian_bots:
            # we'll have enough ore and obsidian in:
            dt = 1 + ceil(max(
                0,
                (geode_bot_ores - ores) / ore_bots,
                (geode_bot_obsidians - obsidians) / obsidian_bots,
            ))
            if concurential(t + dt, geodes + geode_bots * dt, geode_bots + 1,  min_geodes):
                queue.push(geode_bots + 1, (
                    t + dt,
                    ores - geode_bot_ores + ore_bots * dt,
                    clays + clay_bots * dt,
                    obsidians - geode_bot_obsidians + obsidian_bots * dt,
                    geodes + geode_bots * dt,
                    ore_bots, clay_bots, obsidian_bots, geode_bots + 1,
                ))
        # Obsidian bots production is possible only if we have clay bots to produce clay
        if clay_bots and obsidian_bots <= max_obsidian_bots:
            # we'll have enough ore and clay in:
            dt = 1 + ceil(max(
                0, (obsidian_bot_ores - ores) / ore_bots, (obsidian_bot_clays - clays) / clay_bots,
            ))
            if concurential(t + dt, geodes + geode_bots * dt, geode_bots, min_geodes):
                queue.push(geode_bots, (
                    t + dt,
                    ores - obsidian_bot_ores + ore_bots * dt,
                    clays - obsidian_bot_clays + clay_bots * dt,
                    obsidians + obsidian_bots * dt,
                    geodes + geode_bots * dt,
                    ore_bots, clay_bots, obsidian_bots + 1, geode_bots,
                ))
        # Clay bots production is always possible but we don't necessarily need too many
        if clay_bots <= max_clay_bots: 
            # we'll have enough ore in:
            dt = 1 + ceil(max(0, (clay_bot_ores - ores) / ore_bots))
            if concurential(t + dt, geodes + geode_bots * dt, geode_bots, min_geodes):
                queue.push(geode_bots, (
                    t + dt,
                    ores - clay_bot_ores + ore_bots * dt,
                    clays + clay_bots * dt,
                    obsidians + obsidian_bots * dt,
                    geodes + geode_bots * dt,
                    ore_bots, clay_bots + 1, obsidian_bots, geode_bots,
                ))
        # Ore bots production is always possible but we don't necessarily need too many
        if ore_bots <= max_ore_bots:
            dt = 1 + ceil(max(0, (ore_bot_ores - ores) / ore_bots))
            if concurential(t + dt, geodes + geode_bots * dt, geode_bots, min_geodes):
                queue.push(geode_bots, (
                    t + dt,
                    ores - ore_bot_ores + ore_bots * dt,
                    clays + clay_bots * dt,
                    obsidians + obsidian_bots * dt,
                    geodes + geode_bots * dt,
                    ore_bots + 1, clay_bots, obsidian_bots, geode_bots,
                ))
    return min_geodes


def part1(data):
    return sum(
        b_id * crack_geodes(*blueprint)
        for b_id, blueprint in parse(data).items()
    )


assert (result := part1(test_data)) == 33, f"{result=}"
print("Part 1:", part1(adv.input()))

DEADLINE = 32

assert (result := crack_geodes(*parse(test_data)[1])) == 56, f"bp 1: {result}"
assert (result := crack_geodes(*parse(test_data)[2])) == 62, f"bp 2: {result}"

def part2(data):
    blueprints = parse(data)
    return crack_geodes(*blueprints[1]) * crack_geodes(*blueprints[2]) * crack_geodes(*blueprints[3])

print("Part 2:", part2(adv.input()))
