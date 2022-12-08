#! /usr/bin/env python

from functools import reduce
from itertools import product, zip_longest
from operator import mul

import advent_of_code as adv


test_data = """\
30373
25512
65332
33549
35390
"""

def to_elevation_map(data):
    return [[int(tree) for tree in line] for line in data.splitlines()]


def count_visible(tree_map):
    transposed_map = [list(t) for t in zip(*tree_map)]
    height = len(tree_map)
    width = len(tree_map[0])
    visibles = (height + width - 2) * 2
    for x, y in product(range(1, width-1), range(1, height-1)):
        tree = tree_map[y][x]
        if (
            max(tree_map[y][:x]) < tree or max(tree_map[y][x+1:]) < tree
            or max(transposed_map[x][:y]) < tree or max(transposed_map[x][y+1:]) < tree
        ):
            visibles += 1
    return visibles


assert count_visible(to_elevation_map(test_data)) == 21
print("Part 1:", count_visible(adv.input(to_elevation_map)))


def scenic_score(tree_map, x, y):
    height = len(tree_map)
    width = len(tree_map[0])
    tree = tree_map[y][x]
    accumulators = [0, 0, 0, 0]
    for accu, ray in enumerate((
        zip_longest(range(-1, -x-1, -1), [], fillvalue=0),
        zip_longest(range(1, width-x), [], fillvalue=0),
        zip_longest([], range(-1, -y-1, -1), fillvalue=0),
        zip_longest([], range(1, height-y), fillvalue=0),
    )):
        for dx, dy in ray:
            accumulators[accu] += 1
            if tree_map[y+dy][x+dx] >= tree:
                break
    return reduce(mul, accumulators)


def best_tree(tree_map):
    height = len(tree_map)
    width = len(tree_map[0])
    return max(
        scenic_score(tree_map, x, y) for x, y in product(range(1, width-1), range(1, height-1))
    )


assert best_tree(to_elevation_map(test_data)) == 8
print("Part 2:", best_tree(adv.input(to_elevation_map)))

