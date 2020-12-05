#! /usr/bin/env python3

import os.path
import advent_of_code as adv


test_map = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip().splitlines()


def count_trees(tree_map, dx, dy):
    height = len(tree_map)
    width = len(tree_map[0])
    x, y = 0, 0
    trees = 0
    while y < height:
        if tree_map[y][x % width] == "#":
            trees += 1
        x += dx
        y += dy
    return trees


assert count_trees(test_map, 3, 1) == 7

tree_map = adv.input(int(os.path.basename(os.path.dirname(__file__))), adv.to_list_of_str)
print("Part 1:", count_trees(tree_map, 3, 1))


check_slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
product = 1
for dx, dy in check_slopes:
    product *= count_trees(test_map, dx, dy)

assert product == 336

product = 1
for dx, dy in check_slopes:
    product *= count_trees(tree_map, dx, dy)
print("Part 2:", product)
