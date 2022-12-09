#! /usr/bin/env python

import advent_of_code as adv

test_data = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""


def to_motions(data):
    return [
        (move, int(distance)) for line in data.splitlines() for move, distance in [line.split()]
    ]


DX = {'R': 1, 'U': 0, 'L': -1, 'D': 0}
DY = {'R': 0, 'U': 1, 'L': 0, 'D': -1}


def move_knot(xh, yh, xt, yt):
    if xh-1 <= xt <= xh+1 and yh-1 <= yt <= yh+1:
        pass  # Touching -> do nothing
    elif yh > yt and xh == xt:
        yt = yh - 1  # Same column and above
    elif yh < yt and xh == xt:
        yt = yh + 1  # Same column and below
    elif xh > xt and yh == yt:
        xt = xh - 1  # Same line and right
    elif xh < xt and yh == yt:
        xt = xh + 1  # Same line and right
    elif yh > yt and xh-1 == xt:
        xt, yt = xh, yh - 1  # Next column and above
    elif yh < yt and xh-1 == xt:
        xt, yt = xh, yh + 1  # Next column and below
    elif yh > yt and xh+1 == xt:
        xt, yt = xh, yh - 1  # Previous column and above
    elif yh < yt and xh+1 == xt:
        xt, yt = xh, yh + 1  # Previous column and below
    elif xh > xt and yh-1 == yt:
        xt, yt = xh - 1, yh  # Line above and right
    elif xh < xt and yh-1 == yt:
        xt, yt = xh + 1, yh  # Line above and left
    elif xh > xt and yh+1 == yt:
        xt, yt = xh - 1, yh  # Line below and right
    elif xh < xt and yh+1 == yt:
        xt, yt = xh + 1, yh  # Line below and left
    elif xh > xt and yh > yt:
        xt, yt = xh - 1, yh - 1  # Straight upper right diagonal
    elif xh > xt and yh < yt:
        xt, yt = xh - 1, yh + 1  # Straight down right diagonal
    elif xh < xt and yh > yt:
        xt, yt = xh + 1, yh - 1  # Straight upper left diagonal
    elif xh < xt and yh < yt:
        xt, yt = xh + 1, yh + 1  # Straight down left diagonal
    else:
        assert False, "Unexpected configuration"
    return xt, yt


def simulate(moves, length):
    rope = [(0, 0)] * length
    visited = {rope[-1]}
    for direction, distance in moves:
        for step in range(distance):
            xh, yh = rope[0]
            xh += DX[direction]
            yh += DY[direction]
            rope[0] = (xh, yh)
            for i, (xt, yt) in enumerate(rope[1:], 1):
                xt, yt = move_knot(xh, yh, xt, yt)
                rope[i] = (xt, yt)
                xh, yh = xt, yt
            visited.add((xt, yt))
    return len(visited)


assert simulate(to_motions(test_data), 2) == 13
print("Part 1:", simulate(adv.input(to_motions), 2))

test_data2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

assert simulate(to_motions(test_data), 10) == 1
assert simulate(to_motions(test_data2), 10) == 36
print("Part 2:", simulate(adv.input(to_motions), 10))
