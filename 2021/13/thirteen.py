#! /usr/bin/env python

from pathlib import Path
import advent_of_code as adv


def parse(text):
    points, folds = text.strip().split('\n\n')
    points = {tuple(map(int, line.split(','))) for line in points.splitlines()}
    folds = [(line.split('=')[0][-1], int(line.split('=')[1])) for line in folds.splitlines()]
    return points, folds


test_data = parse((Path(__file__).parent / 'test_data').read_text())
data = adv.input(Path(__file__).parent.name, parse)


def fold_point(point, axis, position):
    point = list(point)
    axis = {'x': 0, 'y': 1}[axis]
    if point[axis] > position:
        point[axis] = position - (point[axis] - position)
    return tuple(point)


def fold(points, folds):
    for axis, position in folds:
        points = {fold_point(point, axis, position) for point in points}
    return points


def print_points(points):
    max_x, max_y = 0, 0
    for x, y in points:
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    for y in range(max_y + 1):
        print(''.join('#' if (x, y) in points else ' ' for x in range(max_x + 1)))


points, folds = test_data
assert len(fold(points, folds[:1])) == 17
points, folds = data
print("Part 1:", len(fold(points, folds[:1])))

print("Part 2:")
print_points(fold(*data))
