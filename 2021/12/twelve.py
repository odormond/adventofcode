#! /usr/bin/env python

from pathlib import Path
import advent_of_code as adv


def to_graph(text):
    nodes, edges = set(), set()
    for line in text.splitlines():
        a, b = line.split('-')
        nodes.add(a)
        nodes.add(b)
        edges.add(tuple(sorted((a, b))))
    return nodes, edges


test_data_1 = to_graph(Path('test_data_1').read_text())
test_data_2 = to_graph(Path('test_data_2').read_text())
test_data_3 = to_graph(Path('test_data_3').read_text())
data = adv.input(Path(__file__).parent.name, to_graph)


def edges_from(source, edges):
    for edge in edges:
        if source in edge:
            yield edge


def find_path(nodes, edges, with_extra_small=False):
    paths = []
    queue = [(False, ['start'])]
    while queue:
        orig_used_extra, path = queue.pop(0)
        source = path[-1]
        for edge in edges_from(source, edges):
            used_extra = orig_used_extra
            destination = (set(edge) - {source}).pop()
            if destination == 'start':
                continue
            if destination.islower() and destination in path:
                # Would pass twice by a small cave
                if with_extra_small and used_extra is False:
                    used_extra = True
                else:
                    continue
            if destination == 'end':
                paths.append(path+['end'])
                continue  # A complete path
            queue.append((used_extra, path + [destination]))
    return paths


assert len(find_path(*test_data_1)) == 10
assert len(find_path(*test_data_2)) == 19
assert len(find_path(*test_data_3)) == 226
print("Part 1:", len(find_path(*data)))

assert len(find_path(*test_data_1, True)) == 36
assert len(find_path(*test_data_2, True)) == 103
assert len(find_path(*test_data_3, True)) == 3509
print("Part 2:", len(find_path(*data, True)))
