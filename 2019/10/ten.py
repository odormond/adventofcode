#! /usr/bin/env python

from math import atan2, pi, hypot

import advent_of_code as adv


def to_asteroids(text):
    return [
        (x, y)
        for y, line in enumerate(text.splitlines())
        for x, asteroid in enumerate(line.strip())
        if asteroid == '#'
    ]


def find_best_spot(asteroids):
    best_visibles = 0
    best_asteroid = None
    for x, y in asteroids:
        angles = [atan2(ox - x, oy - y) for ox, oy in asteroids if (ox, oy) != (x, y)]
        visibles = len(set(angles))
        if visibles > best_visibles:
            best_visibles = visibles
            best_asteroid = x, y
    return best_visibles, best_asteroid


assert find_best_spot(to_asteroids(".#..#\n.....\n#####\n....#\n...##")) == (8, (3, 4))
assert find_best_spot(to_asteroids("......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####")) == (33, (5, 8))
assert find_best_spot(to_asteroids("#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.")) == (35, (1, 2))
assert find_best_spot(to_asteroids(".#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..")) == (41, (6, 3))
big_test = ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##"
assert find_best_spot(to_asteroids(big_test)) == (210, (11, 13))

asteroids = adv.input(10, to_asteroids)
visibles, asteroid = find_best_spot(asteroids)
print("Part one:", visibles)


def vaporize(asteroids, base):
    def angle_dist(asteroid):
        bx, by = base
        x, y = asteroid
        dx = x - bx
        dy = y - by
        a = pi/2 - atan2(-dy, dx)
        if a < 0:
            a += 2 * pi
        return a, hypot(dx, dy)

    asteroids = sorted((a for a in asteroids if a != base), key=angle_dist)
    prev_angle = None
    watchdog = len(asteroids)
    while asteroids:
        asteroid = asteroids.pop(0)
        angle, dist = angle_dist(asteroid)
        if angle != prev_angle:
            yield asteroid
            prev_angle = angle
            watchdog = len(asteroids)
        else:
            asteroids.append(asteroid)  # For next turn
            watchdog -= 1
        if watchdog == 0:
            prev_angle = None


order = list(vaporize(to_asteroids(big_test), (11, 13)))
assert order[0] == (11, 12), order[0]
assert order[1] == (12, 1), order[1]
assert order[2] == (12, 2), order[2]
assert order[9] == (12, 8), order[9]
assert order[19] == (16, 0), order[19]
assert order[49] == (16, 9), order[49]
assert order[99] == (10, 16), order[99]
assert order[198] == (9, 6), order[198]
assert order[199] == (8, 2), order[199]
assert order[200] == (10, 9), order[200]
assert order[298] == (11, 1), order[298]
assert len(order) == 299


order = list(vaporize(asteroids, asteroid))
x, y = order[199]
print("Part two:", x * 100 + y)
