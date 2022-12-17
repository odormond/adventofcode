#! /usr/bin/env python

from itertools import product
import re

import advent_of_code as adv

INPUT_RE = re.compile(r'Valve (?P<valve>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<others>.+)')

test_data = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


def parse(data):
    nodes = {}
    edges = {}
    for line in data.splitlines():
        match = INPUT_RE.match(line)
        nodes[node := match.group('valve')] = int(match.group('rate'))
        edges[node] = match.group('others').split(', ')
    moves = {}
    for start, end in product(nodes, nodes):
        if start == end:
            continue
        if nodes[end] == 0:
            continue  # Useless to move to a stuck valve
        if nodes[start] == 0 and start != 'AA':
            continue  # We don't stop on stuck valve except AA so no need to record moves
        if end in edges[start]:
            moves[(start, end)] = 1 + 1  # Direct move takes 1 minute + 1 to open the valve
            continue
        # We need to find a longer path but we want the shortest
        candidates = [(start, connection) for connection in edges[start]]
        while candidates:
            path = candidates.pop(0)
            if end in edges[path[-1]]:
                moves[(start, end)] = len(path) + 1  # +1 for opening the valve
                break
            for connection in edges[path[-1]]:
                if connection not in path:
                    candidates.append(path + (connection,))
    return nodes, sorted((cost, start, end) for (start, end), cost in moves.items())


def part1(nodes, moves):
    finals = set()
    DEADLINE = 30
    queue = {('AA', 0,  ())}
    while queue:
        next_queue = set()
        for node, t, opened in queue:
            done = dict(opened)
            progress = False
            for cost, start, end in moves:
                if start != node or end in done or t + cost >= DEADLINE:
                    continue
                next_state = (end, t + cost, tuple(sorted(opened + ((end, DEADLINE - t - cost),))))
                assert next_state not in next_queue
                next_queue.add(next_state)
                progress = True
            if not progress:
                finals.add(opened)
        queue = next_queue
    return max(
        sum(nodes[node] * opened_for for node, opened_for in opened) for opened in finals
    )


assert (result := part1(*parse(test_data))) == 1651, f"{result=}"
print("Part 1:", part1(*parse(adv.input())))


def part2(nodes, moves):
    finals = set()
    DEADLINE = 26
    queue = {(0, 'AA', 0, 'AA', ())}
    while queue:
        next_queue = set()
        for current_t, node1, next_t, node2, opened in queue:
            done = dict(opened)
            progress = False
            for cost, start, end in moves:
                if start != node1 or end in done or current_t + cost >= DEADLINE:
                    continue
                next_opened = tuple(sorted(opened + ((end, DEADLINE - current_t - cost),)))
                if next_t < current_t + cost:
                    # Node 2 act next
                    next_state = (next_t, node2, current_t + cost, end, next_opened)
                else:
                    # Node 1 has time to make a second move before node2 is done
                    next_state = (current_t + cost, end, next_t, node2, next_opened)
                next_queue.add(next_state)
                progress = True
            if not progress:
                finals.add(opened)
        queue = next_queue
    return max(
        sum(nodes[node] * opened_for for node, opened_for in opened) for opened in finals
    )


assert (result := part2(*parse(test_data))) == 1707, f"{result=}"
print("Part 2:", part2(*parse(adv.input())))
