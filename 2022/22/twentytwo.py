#! /usr/bin/env python

import re

import advent_of_code as adv

test_data = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""


def move_or_turn(m):
    try:
        return int(m)
    except ValueError:
        return m


def parse(data):
    map_, moves = data.split('\n\n')
    grid = {}
    width = height = 0
    start = None
    for y, line in enumerate(map_.splitlines()):
        height = max(height, y)
        for x, c in enumerate(line):
            width = max(width, x)
            if c == ' ':
                continue
            if start is None:
                start = x, y
            grid[(x, y)] = c
    width += 1
    height += 1
    moves = [move_or_turn(m) for m in re.findall(r'(\d+|[LR])', moves)]
    return grid, start, (width, height), moves


TEST_WRAP_RULES_1 = [
    # facing, x, y, new_facing_x_y(x, y)
    (2, 7, (0, 3), lambda x, y: (2, 11, y)),  # a <
    (0, 12, (0, 3), lambda x, y: (0, 8, y)),  # b >
    (2, -1, (4, 7), lambda x, y: (2, 11, y)),  # c <
    (0, 12, (4, 7), lambda x, y: (0, 0, y)),  # d >
    (2, 7, (8, 11), lambda x, y: (2, 15, y)),  # e <
    (0, 16, (8, 11), lambda x, y: (0, 8, y)),  # b >
    (3, (8, 11), -1, lambda x, y: (3, x, 11)),  # f ^
    (3, (0, 3), 3, lambda x, y: (3, x, 7)),  # f ^
    (3, (4, 7), 3, lambda x, y: (3, x, 7)),  # a ^
    (1, (0, 3), 8, lambda x, y: (1, x, 4)),  # g v
    (1, (4, 7), 8, lambda x, y: (1, x, 4)),  # e v
    (3, (12, 15), 7, lambda x, y: (3, x, 11)),  # d ^
    (1, (8, 11), 12, lambda x, y: (1, x, 0)),  # g v
    (1, (12, 15), 12, lambda x, y: (1, x, 8)),  # c v
]
"""
              1
  0   4   8   2
          fff
0        a111b
         a111b
         a111b
  fff aaa
4c222 333 444d
 c222 333 444d
 c222 333 444d
  ggg eee     ddd
8        e555 666b
         e555 666b
         e555 666b
          ggg ccc
"""
TEST_WRAP_RULES_2 = [
    # facing, x, y, new_facing_x_y(x, y)
    (2, 7, (0, 3), lambda x, y: (1, 4 + x, 4)),  # a <
    (0, 12, (0, 3), lambda x, y: (2, 15, 11 - x)),  # b >
    (2, -1, (4, 7), lambda x, y: (3, 19 - y, 11)),  # c <
    (0, 12, (4, 7), lambda x, y: (1, 19 - y, 8)),  # d >
    (2, 7, (8, 11), lambda x, y: (3, 15 - y, 7)),  # e <
    (0, 16, (8, 11), lambda x, y: (2, 11, 11 - y)),  # b >
    (3, (8, 11), -1, lambda x, y: (1, 11 - x, 4)),  # f ^
    (3, (0, 3), 3, lambda x, y: (1, 11 - x, 0)),  # f ^
    (3, (4, 7), 3, lambda x, y: (0, 8, x - 4)),  # a ^
    (1, (0, 3), 8, lambda x, y: (3, 11 - x, 11)),  # g v
    (1, (4, 7), 8, lambda x, y: (0, 8, 19 - x)),  # e v
    (3, (12, 15), 7, lambda x, y: (2, 11, 19 - x)),  # d ^
    (1, (8, 11), 12, lambda x, y: (3, 11 - x, 7)),  # g v
    (1, (12, 15), 12, lambda x, y: (0, 19 - x, 0)),  # c v
]

WRAP_RULES_1 = [
    # facing, x, y, new_facing_x_y(x, y)
    (2, 49, (0, 49), lambda x, y: (2, 149, y)),  # a <
    (0, 150, (0, 49), lambda x, y: (0, 50, y)),  # b >
    (2, 49, (50, 99), lambda x, y: (2, 99, y)),  # c <
    (0, 100, (50, 99), lambda x, y: (0, 50, y)),  # d >
    (2, -1, (100, 149), lambda x, y: (2, 99, y)),  # a <
    (0, 100, (100, 149), lambda x, y: (0, 0, y)),  # b >
    (2, -1, (150, 199), lambda x, y: (2, 49, y)),  # e <
    (0, 50, (150, 199), lambda x, y: (0, 0, y)),  # f >
    (3, (50, 99), -1, lambda x, y: (3, x, 149)),  # e ^
    (3, (100, 149), -1, lambda x, y: (3, x, 49)),  # g ^
    (1, (100, 149), 50, lambda x, y: (1, x, 0)),  # d v
    (3, (0, 49), 99, lambda x, y: (3, x, 199)),  # c ^
    (1, (50, 99), 150, lambda x, y: (1, x, 0)),  # f v
    (1, (0, 49), 200, lambda x, y: (1, x, 100)),  # g v
]
"""
     eee ggg
    a111 222b
    a111 222b
    a111 222b
         ddd
    c333d
    c333d
    c333d
 ccc    
a444 555b
a444 555b
a444 555b
     fff
e666f
e666f
e666f
 ggg
"""
WRAP_RULES_2 = [
    # facing, x, y, new_facing_x_y(x, y)
    (2, 49, (0, 49), lambda x, y: (0, 0, 149 - y)),  # a <
    (0, 150, (0, 49), lambda x, y: (2, 99, 149 - y)),  # b >
    (2, 49, (50, 99), lambda x, y: (1, y - 50, 100)),  # c <
    (0, 100, (50, 99), lambda x, y: (3, 50 + y, 49)),  # d >
    (2, -1, (100, 149), lambda x, y: (0, 50, 149 - y)),  # a <
    (0, 100, (100, 149), lambda x, y: (2, 149, 149 - y)),  # b >
    (2, -1, (150, 199), lambda x, y: (1, y - 100, 0)),  # e <
    (0, 50, (150, 199), lambda x, y: (3, y - 100, 149)),  # f >
    (3, (50, 99), -1, lambda x, y: (0, 0, 100 + x)),  # e ^
    (3, (100, 149), -1, lambda x, y: (3, x - 100, 199)),  # g ^
    (1, (100, 149), 50, lambda x, y: (2, 99, x - 50)),  # d v
    (3, (0, 49), 99, lambda x, y: (0, 50, x + 50)),  # c ^
    (1, (50, 99), 150, lambda x, y: (2, 49, x + 100)),  # f v
    (1, (0, 49), 200, lambda x, y: (1, x + 100, 0)),  # g v
]


track = {}


def do_move(x, y, facing, steps, grid, wrappings):
    for step in range(steps):
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][facing]
        nf, nx, ny = facing, x + dx, y + dy
        for toward, x_range, y_range, new_xy in wrappings:
            if facing != toward:
                continue
            if isinstance(x_range, int) and nx == x_range and y_range[0] <= ny <= y_range[1]:
                nf, nx, ny = new_xy(nx, ny)
                break
            elif isinstance(y_range, int) and x_range[0] <= nx <= x_range[1] and ny == y_range:
                nf, nx, ny = new_xy(nx, ny)
                break
        if grid[(nx, ny)] == '#':
            track[(x, y)] = facing
            return facing, x, y
        facing, x, y = nf, nx, ny
        track[(x, y)] = facing
    track[(x, y)] = facing
    return facing, x, y


def walk(data, wrappings):
    grid, (x, y), (width, height), moves = parse(data)
    facing = 0
    track[(x, y)] = facing
    for move in moves:
        if move == 'L':
            facing = (facing - 1) % 4
        elif move == 'R':
            facing = (facing + 1) % 4
        else:
            facing, x, y = do_move(x, y, facing, move, grid, wrappings)
        track[(x, y)] = facing
    # print('\n'.join(''.join('>v<^'[track[(x, y)]] if (x, y) in track else grid.get((x, y), ' ') for x in range(width)) for y in range(height)))
    return 1000 * (y+1) + 4 * (x+1) + facing


assert (result := walk(test_data, TEST_WRAP_RULES_1)) == 6032, f"{result=}"
print("Part 1:", walk(adv.input(), WRAP_RULES_1))

assert (result := walk(test_data, TEST_WRAP_RULES_2)) == 5031, f"{result=}"
print("Part 2:", walk(adv.input(), WRAP_RULES_2))
