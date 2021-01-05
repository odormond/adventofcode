#! /usr/bin/env pypy

TEST = (
    ([3, 8, 9, 1, 2, 5, 4, 6, 7], 10, '92658374'),
    ([3, 8, 9, 1, 2, 5, 4, 6, 7], 100, '67384529'),
)
PUZZLE = [3, 2, 7, 4, 6, 5, 1, 8, 9]


def play(circle, steps, n):
    circle = [i - 1 for i in circle]
    while steps:
        steps -= 1
        moved = circle[1:4]
        current = circle[0]
        del circle[:4]
        dest = (current - 1) % n
        while dest in moved:
            dest = (dest - 1) % n
        idx = circle.index(dest) + 1
        circle[idx:idx] = moved
        circle.append(current)
    return [i + 1 for i in circle]


def check(circle):
    one = circle.index(1)
    return ''.join(map(str, circle[one + 1 :] + circle[:one]))


for start, steps, result in TEST:
    assert check(play(start, steps, 9)) == result

print("Part 1:", check(play(PUZZLE, 100, 9)))

circle = play([3, 8, 9, 1, 2, 5, 4, 6, 7] + list(range(10, 1000001)), 10000000, 1000000)
i = circle.index(1)
a = circle[(i + 1) % 1000000]
b = circle[(i + 2) % 1000000]
assert (a, b) == (934001, 159792)

circle = play(PUZZLE + list(range(10, 1000001)), 10000000, 1000000)
i = circle.index(1)
a = circle[(i + 1) % 1000000]
b = circle[(i + 2) % 1000000]
print("Part 2:", a * b)
