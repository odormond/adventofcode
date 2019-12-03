#! /usr/bin/env python

import advent_of_code as adv


MOVES = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


def line_positions(moves):
    x, y = 0, 0
    for move in moves.split(','):
        direction = move[0]
        steps = int(move[1:])
        dx, dy = MOVES[direction]
        for i in range(steps):
            x += dx
            y += dy
            yield (x, y)


test_data = (
    ("R8,U5,L5,D3\nU7,R6,D4,L4", 6, 30),
    ("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83", 159, 610),
    ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135, 410),
)
for lines, expect_part_one, _ in test_data:
    line1, line2 = (set(line_positions(line)) for line in lines.splitlines())
    closest = min(map(lambda p: sum(map(abs, p)), line1.intersection(line2)))
    assert closest == expect_part_one, f"{closest} != {expect_part_one}"


data = adv.input(3, lambda x: x)

line1, line2 = (set(line_positions(line)) for line in data.splitlines())
closest = min(map(lambda p: sum(map(abs, p)), line1.intersection(line2)))

print("Part one:", closest)


for lines, _, expect_part_two in test_data:
    line1, line2 = map(list, (line_positions(line) for line in lines.splitlines()))
    delay = min(
        line1.index(intersection) + line2.index(intersection) + 2  # because first step is index 0
        for intersection in set(line1).intersection(set(line2))
    )
    assert delay == expect_part_two, f"{delay} != {expect_part_two}"


line1, line2 = map(list, (line_positions(line) for line in data.splitlines()))
delay = min(
    line1.index(intersection) + line2.index(intersection) + 2  # because first step is index 0
    for intersection in set(line1).intersection(set(line2))
)

print("Part two:", delay)
