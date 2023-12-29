#! /usr/bin/env python

from collections import defaultdict

import advent_of_code as adv

test_data = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""


def parse(data):
    return {
        (r, c): g
        for r, line in enumerate(data.splitlines()) for c, g in enumerate(line)
        if g != '#'
    }


def find_paths(grid):
    start = list(grid)[0]
    end = list(grid)[-1]
    segments = defaultdict(set)
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        r, c = path[-1]
        extensions = [
            target
            for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0))
            if (target := (r + dr, c + dc)) in grid
            and ((target != path[-2]) if len(path) >= 2 else True)
            and (
                grid[target] == '.'
                or grid[target] == '>' and dr == 0 and dc == 1
                or grid[target] == '<' and dr == 0 and dc == -1
                or grid[target] == '^' and dr == -1 and dc == 0
                or grid[target] == 'v' and dr == 1 and dc == 0
            )
        ]
        if len(extensions) == 1:
            queue.append(path + extensions)
        elif extensions:
            segment = tuple(path)
            if segment in segments[path[0]]:
                continue
            segments[path[0]].add(segment)
            for next_step in extensions:
                queue.append([path[-1], next_step])
        elif path[-1] == end:
            segment = tuple(path)
            if segment in segments[path[0]]:
                continue
            segments[path[0]].add(segment)
    exit_paths = []
    queue = [(start,)]
    while queue:
        path = queue.pop(0)
        for segment in segments[path[-1]]:
            if segment[-1] == end:
                exit_paths.append(path + segment[1:])
            elif len(set(segment) & set(path)) == 1:
                queue.insert(0, path + segment[1:])
    return exit_paths


def part1(data):
    grid = parse(data)
    paths = find_paths(grid)
    return len(sorted(paths, key=len)[-1]) - 1



assert (result := part1(test_data)) == 94, f"{result=}"
print("Part 1:", part1(adv.input()))


def graph(grid):
    start = list(grid)[0]
    end = list(grid)[-1]
    segments = defaultdict(set)
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        r, c = path[-1]
        extensions = [
            target
            for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0))
            if (target := (r + dr, c + dc)) in grid
            and ((target != path[-2]) if len(path) >= 2 else True)
            and (
                grid[target] == '.'
                or grid[target] == '>' and dr == 0 and dc == 1
                or grid[target] == '<' and dr == 0 and dc == -1
                or grid[target] == '^' and dr == -1 and dc == 0
                or grid[target] == 'v' and dr == 1 and dc == 0
            )
        ]
        if len(extensions) == 1:
            queue.append(path + extensions)
        elif extensions:
            segment = tuple(path)
            if segment in segments[path[0]]:
                continue
            segments[path[0]].add(segment)
            for next_step in extensions:
                queue.append([path[-1], next_step])
        elif path[-1] == end:
            segment = tuple(path)
            if segment in segments[path[0]]:
                continue
            segments[path[0]].add(segment)
    nodes = set(segments) | {end}
    edges = {tuple((*sorted((p[0], p[-1])), len(p) - 1)) for s in segments.values() for p in s}
    return nodes, edges, start, end



def connected(edges, node, path):
    for a, b, w in edges:
        if a == node and b not in path:
            yield b, w
        elif b == node and a not in path:
            yield a, w


def find_paths(nodes, edges, path):
    middle = len(path) // 2
    start = path[middle - 1]
    end = path[middle]
    if start == end:
        return [0]
    edge = tuple(sorted((start, end)))
    for a, b, w in edges:
        if (a, b) == edge:
            return [w]
    return sorted(
        w + l + v
        for next_hop, w in connected(edges, start, path)
        for prev_hop, v in connected(edges, end, path)
        for l in find_paths(nodes, edges, path[:middle] + [next_hop, prev_hop] + path[middle:])
    )[-1:]


def part2(data):
    grid = {k: '.' for k in parse(data)}
    nodes, edges, start, end = graph(grid)
    return find_paths(nodes, edges, [start, end])[-1]


assert (result := part2(test_data)) == 154, f"{result=}"
print("Part 2:", part2(adv.input()))
