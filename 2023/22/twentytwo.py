#! /usr/bin/env python

from itertools import product

import advent_of_code as adv

test_data = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

def parse(data):
    for line in data.splitlines():
        corner1, corner2 = line.split('~')
        x1, y1, z1 = [int(v) for v in corner1.split(',')]
        x2, y2, z2 = [int(v) for v in corner2.split(',')]
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        z1, z2 = sorted([z1, z2])
        yield {cube for cube in product(range(x1, x2+1), range(y1, y2+1), range(z1, z2+1))}


def fall(bricks):
    bricks = sorted(bricks, key=lambda brick: min(z for x, y, z in brick))
    setteled = []
    moved = 0
    for brick in bricks:
        did_move = False
        while True:
            z = min(z for x, y, z in brick)
            if z == 1:
                setteled.append(brick)
                break
            falling_brick = {(x, y, z-1) for x, y, z in brick}
            if any(settled_brick & falling_brick for settled_brick in setteled):
                setteled.append(brick)
                break
            brick = falling_brick
            did_move = True
        if did_move:
            moved += 1
    return setteled, moved


def solve(data):
    bricks = list(parse(data))
    bricks, moved = fall(bricks)
    assert fall(bricks)[1] == 0
    disintegratable = 0
    would_fall = 0
    for i, brick in enumerate(bricks):
        others = bricks[:i] + bricks[i+1:]
        if (moved := fall(others)[1]) == 0:
            disintegratable += 1
        would_fall += moved
    return disintegratable, would_fall


assert (result := solve(test_data)) == (5, 7), f"{result=}"
print("Part 1 & 2:", solve(adv.input()))
