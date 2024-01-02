#! /usr/bin/env python

from random import choice

import advent_of_code as adv

test_data = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

def parse(data):
    vertices = set()
    edges = set()
    for line in data.splitlines():
        a, bs = line.split(':')
        vertices.add(a)
        for b in bs.split():
            vertices.add(b)
            edges.add((a, b))
    return vertices, edges


def contract(V, E):
    a, b = choice(E)
    V.remove(a)
    V.remove(b)
    contraction = f'{a} {b}'
    V.add(contraction)
    E = [e for e in E if e != (a, b) and e != (b, a)]
    removed = []
    added = []
    for c, d in E:
        if c in (a, b):
            added.append((contraction, d))
            removed.append((c, d))
        elif d in (a, b):
            added.append((c, contraction))
            removed.append((c, d))
    for e in removed:
        E.remove(e)
    E += added
    return V, E


def part1(data):
    attempts = 0
    vertices, edges = parse(data)
    edges = list(edges)
    E = edges
    while len(E) > 3:
        attempts += 1
        print(f'\r{attempts}\033[K', end='')
        V = vertices.copy()
        E = edges.copy()
        while len(V) > 2:
            # print(f'\r{attempts}: V: {len(V)}, E: {len(E)}\033[K', end='')
            V, E = contract(V, E)
        if attempts == 10:
            break
    print()
    group1, group2 = E[0]
    return len(group1.split()) * len(group2.split())


assert (result := part1(test_data)) == 54, f"{result=}"
print("Part 1:", part1(adv.input()))
