#! /usr/bin/env python

from collections import Counter, defaultdict
from itertools import combinations, product

import advent_of_code as aoc

test_data = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def parse(data):
    connections = defaultdict(set)
    for connection in data.splitlines():
        a, b = connection.split("-")
        connections[a].add(b)
        connections[b].add(a)
    return connections


def part1(data):
    connections = parse(data)
    count = 0
    t_computers = [computer for computer in connections if computer.startswith("t")]
    non_t_computers = [computer for computer in connections if not computer.startswith("t")]
    for t, (a, b) in product(t_computers, combinations(non_t_computers, 2)):
        if {a, b}.issubset(connections[t]) and {t, a}.issubset(connections[b]):
            count += 1
    for non_t, (a, b) in product(non_t_computers, combinations(t_computers, 2)):
        if {a, b}.issubset(connections[non_t]) and {non_t, a}.issubset(connections[b]):
            count += 1
    for a, b, c in combinations(t_computers, 3):
        if {a, b}.issubset(connections[c]) and {b, c}.issubset(connections[a]):
            count += 1
    return count


assert (result := part1(test_data)) == 7, f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    connections = parse(data)
    inter_connected = set()
    for _, lan in connections.items():
        peers = list(lan)  # Skip the starting computer or it gets counted one time too much
        for other in lan:
            peers += [other, *connections[other]]
        largest = set()
        prev_count = None
        for peer, count in Counter(peers).most_common():
            if prev_count is not None and count < prev_count:
                break
            prev_count = count
            largest.add(peer)
        inter_connected.add(frozenset(largest))
    most_connected = sorted(inter_connected, key=len, reverse=True)[0]
    return ",".join(sorted(most_connected))


assert (result := part2(test_data)) == "co,de,ka,ta", f"{result=}"
print("Part 2:", part2(aoc.input()))
