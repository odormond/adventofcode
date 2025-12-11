#! /usr/bin/env python

from collections import Counter

import advent_of_code as aoc

test_data = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

def parse(data):
    graph = {}
    for line in data.splitlines():
        src, dsts = line.split(": ")
        graph[src] = dsts.split()
    return graph


def paths(start, graph):
    ends = Counter()
    path = [start]
    while path:
        if path[-1] not in graph:
            ends[path[-1]] += 1
            backtrack(path, graph)
        else:
            path += graph[path[-1]][:1]
    return ends


def backtrack(path, graph):
    if len(path) < 2:
        del path[-1]
        return
    alternates = graph[path[-2]]
    next_index = alternates.index(path[-1]) + 1
    for next_node in alternates[next_index:]:
        path[-1] = next_node
        break
    else:
        del path[-1]
        backtrack(path, graph)


def part1(data):
    graph = parse(data)
    return paths("you", graph).total()


assert (result := part1(test_data)) == 5, f"{result=}"
print("Part 1:", part1(aoc.input()))


test_data_2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

def strip(graph, keep):
    while (
        stripped := {
            k: n
            for k, vs in graph.items()
            if (n := [v for v in vs if v in graph] if k not in keep else vs)
        }
    ) != graph:
        graph = stripped
    return graph


def part2(data):
    full_graph = parse(data)
    previous = Counter(["svr"])
    for graph in [
        *sorted((strip(full_graph, (checkpoint,)) for checkpoint in ("dac", "fft")), key=len),
        full_graph
    ]:
        current = Counter()
        for start, count in previous.items():
            ends = paths(start, graph)
            for k in ends:
                ends[k] *= count
            current.update(ends)
        previous = current
    return current.total()


assert (result := part2(test_data_2)) == 2, f"{result=}"
print("Part 2:", part2(aoc.input()))
