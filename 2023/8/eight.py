#! /usr/bin/env python

import math

import advent_of_code as adv

test_data = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

test_data_2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


def parse(data):
    moves, raw_graph = data.split('\n\n')
    moves = [0 if m == 'L' else 1 for m in moves]
    graph = {}
    for line in raw_graph.splitlines():
        src, dests = line.split(' = ')
        left, right = dests[1:-1].split(', ')
        graph[src] = (left, right)
    return moves, graph


def part1(data):
    moves, graph = parse(data)
    pos = 'AAA'
    i = 0
    while pos != 'ZZZ':
        move = moves[i % len(moves)]
        pos = graph[pos][move]
        i += 1
    return i


assert (result := part1(test_data)) == 2, f"{result=}"
assert (result := part1(test_data_2)) == 6, f"{result=}"
print("Part 1:", part1(adv.input()))

test_data_3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

def part2(data):
    moves, graph = parse(data)
    ghosts = [k for k in graph if k.endswith('A')]
    phases = []
    cycles = []
    for ghost in ghosts:
        i = 0
        while not ghost.endswith('Z'):
            move = moves[i % len(moves)]
            ghost = graph[ghost][move]
            i += 1
        phases.append(i)
        move = moves[i % len(moves)]
        ghost = graph[ghost][move]
        i += 1
        while not ghost.endswith('Z'):
            move = moves[i % len(moves)]
            ghost = graph[ghost][move]
            i += 1
        cycles.append(i - phases[-1])
    assert phases == cycles, "Too bad, not that simple"
    return math.lcm(*cycles)


assert (result := part2(test_data_3)) == 6, f"{result=}"
print("Part 2:", part2(adv.input()))
