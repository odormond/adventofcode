#! /usr/bin/env python

import advent_of_code as aoc

test_small = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
test_large = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

def parse(data):
    warehouse, moves = data.split("\n\n")
    warehouse = {
        (l, c): o
        for l, line in enumerate(warehouse.splitlines())
        for c, o in enumerate(line)
        if o != "."
    }
    for pos, obj in warehouse.items():
        if obj == "@":
            robot = pos
            break
    warehouse.pop(robot)
    moves = moves.replace("\n", "")
    return warehouse, robot, moves


def do_move(pos, move):
    l, c = pos
    dl, dc = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}[move]
    return l + dl, c + dc


def step(warehouse, robot, move):
    next_pos = do_move(robot, move)
    if next_pos not in warehouse:
        # Free move
        return warehouse, next_pos
    if warehouse[next_pos] == "#":
        # Wall, cannot move
        return warehouse, robot
    # Attempting to push
    next_obj = do_move(next_pos, move)
    while warehouse.get(next_obj) == "O":
        next_obj = do_move(next_obj, move)
    if next_obj not in warehouse:
        # Successfully pushed the objects
        warehouse[next_obj] = "O"
        warehouse.pop(next_pos)
        return warehouse, next_pos
    # Failed to push
    return warehouse, robot


def part1(data):
    warehouse, robot, moves = parse(data)
    for move in moves:
        warehouse, robot = step(warehouse, robot, move)
    return sum(100 * l + c for (l, c), o in warehouse.items() if o == "O")


assert (result := part1(test_small)) == 2028, f"{result=}"
assert (result := part1(test_large)) == 10092, f"{result=}"
print("Part 1:", part1(aoc.input()))


def parse2(data):
    raw_warehouse, moves = data.split("\n\n")
    warehouse = {}
    for l, line in enumerate(raw_warehouse.splitlines()):
        for c, o in enumerate(line):
            if o == "@":
                robot = l, c * 2
            elif o == "O":
                warehouse[(l, c * 2)] = "["
                warehouse[(l, c * 2 + 1)] = "]"
            elif o == "#":
                warehouse[(l, c * 2)] = "#"
                warehouse[(l, c * 2 + 1)] = "#"
    moves = moves.replace("\n", "")
    return warehouse, robot, moves


def push_in_line(warehouse, robot, move):
    opposite_move = {"<": ">", ">": "<"}[move]
    next_obj = do_move(robot, move)
    while warehouse.get(next_obj) in {"[", "]"}:
        next_obj = do_move(next_obj, move)
    if next_obj not in warehouse:
        # Successfully pushed the objects
        while (prev_obj := do_move(next_obj, opposite_move)) != robot:
            warehouse[next_obj] = warehouse[prev_obj]
            next_obj = prev_obj
        warehouse.pop(next_obj)
        return warehouse, next_obj
    # Blocked by a wall
    return warehouse, robot


def step2(warehouse, robot, move):
    next_pos = do_move(robot, move)
    if next_pos not in warehouse:
        # Free move
        return warehouse, next_pos
    if warehouse[next_pos] == "#":
        # Wall, cannot move
        return warehouse, robot
    # Attempting to push
    if move in "<>":
        return push_in_line(warehouse, robot, move)
    # Pushing vertically
    l, c = next_pos
    to_push = {(l, c) if warehouse[next_pos] == "[" else (l, c - 1)}
    queue = list(to_push)
    while queue:
        l, c = do_move(queue.pop(0), move)
        if warehouse.get((l, c)) == "#" or warehouse.get((l, c + 1)) == "#":
            # blocked
            break
        for dc in (0, -1, 1):
            if warehouse.get((l, c + dc)) == "[":
                # Another box to push too
                queue.append((l, c + dc))
                to_push.add((l, c + dc))
    else:
        # Push them
        for l, c in to_push:
            warehouse.pop((l, c))
            warehouse.pop((l, c + 1))
        for pos in to_push:
            l, c = do_move(pos, move)
            warehouse[(l, c)] = "["
            warehouse[(l, c + 1)] = "]"
        return warehouse, next_pos
    # Failed to push
    return warehouse, robot


def show(warehouse, robot, move):
    print(f"Move {move}:")
    height, width = max(warehouse)
    for l in range(height + 1):
        for c in range(width + 1):
            if (l, c) == robot:
                print("@", end="")
            else:
                print(warehouse.get((l, c), "."), end="")
        print()
    print()

def part2(data):
    warehouse, robot, moves = parse2(data)
    # show(warehouse, robot, None)
    for move in moves:
        warehouse, robot = step2(warehouse, robot, move)
        # show(warehouse, robot, move)
    return sum(100 * l + c for (l, c), o in warehouse.items() if o == "[")


assert (result := part2(test_large)) == 9021, f"{result=}"
print("Part 2:", part2(aoc.input()))
