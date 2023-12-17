#! /usr/bin/env python

from collections import defaultdict

import advent_of_code as adv

test_data = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

def parse(data):
    grid = [[int(c) for c in line] for line in data.splitlines()]
    width = len(grid[0])
    height = len(grid)
    return grid, width, height


def next_move(x, y, width, heigth, history):
    last_moves = [(ax - bx, ay - by) for (ax, ay), (bx, by) in zip(history[1:], history)][-3:]

    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        if 0 <= x + dx < width and 0 <= y + dy < heigth:
            if last_moves == [(dx, dy)] * 3:
                continue
            yield (x + dx, y + dy)


# Need a queue by cell for the histories that can lead to it.
class PriorityQueue:
    def __init__(self):
        self.queue = defaultdict(lambda: defaultdict(list))

    def push(self, priority, cell, history):
        self.queue[priority][cell].append(history)

    def pop(self):
        p = sorted(self.queue)[0]
        cells = self.queue[p]
        cell, histories = cells.popitem()
        history = histories.pop(0)
        if histories:
            cells[cell] = histories
        if not cells:
            del self.queue[p]
        return p, cell, history

    def __bool__(self):
        return bool(self.queue)

    def __len__(self):
        return sum(len(history) for cells in self.queue.values() for history in cells.values())


def show(grid, loss):
    for a, b in zip(grid, loss):
        print(' '.join(f'{g} ({h:3d})' for g, h in zip(a, b)))
    print()


def part1(data):
    grid, width, height = parse(data)
    start = (0, 0)
    end = (width - 1, height - 1)
    visits = defaultdict(set)
    queue = PriorityQueue()
    queue.push(0, start, [(0, 0)])
    while queue:
        loss, (x, y), history = queue.pop()
        if (x, y) in visits and tuple(history[-4:]) in visits[(x, y)]:
            continue
        visits[(x, y)].add(tuple(history[-4:]))
        for (c, r) in next_move(x, y, width, height, history):
            if (c, r) in history:
                continue
            next_loss = loss + grid[r][c]
            queue.push(next_loss, (c, r), history + [(c, r)])
            if (c, r) == end:
                return next_loss


assert (result := part1(test_data)) == 102, f"{result=}"
print("Part 1:", part1(adv.input()))


def next_move(x, y, width, height, history):
    last_moves = [(ax - bx, ay - by) for (ax, ay), (bx, by) in zip(history[1:], history)]
    if last_moves and last_moves[-4:] != last_moves[-1:] * 4:
        dx, dy = last_moves[-1]
        if 0 <= x + dx < width and 0 <= y + dy < height:
            yield (x + dx, y + dy)
        return
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        if 0 <= x + dx < width and 0 <= y + dy < height:
            if len(last_moves) >= 10 and last_moves[-10:] == [(dx, dy)] * 10:
                continue
            yield (x + dx, y + dy)


def part2(data):
    grid, width, height = parse(data)
    start = (0, 0)
    end = (width - 1, height - 1)
    visits = defaultdict(set)
    queue = PriorityQueue()
    queue.push(0, start, [(0, 0)])
    while queue:
        loss, (x, y), history = queue.pop()
        if (x, y) in visits and tuple(history[-11:]) in visits[(x, y)]:
            continue
        visits[(x, y)].add(tuple(history[-11:]))
        for (c, r) in next_move(x, y, width, height, history):
            if (c, r) in history:
                continue
            next_loss = loss + grid[r][c]
            next_history = history + [(c, r)]
            queue.push(next_loss, (c, r), next_history)
            if (c, r) == end:
                last_moves = [
                    (ax - bx, ay - by)
                    for (ax, ay), (bx, by) in zip(next_history[-4:], next_history[-5:])
                ]
                if last_moves == last_moves[-1:] * 4:
                    return next_loss


test_data_2 = """\
111111111111
999999999991
999999999991
999999999991
999999999991
"""

assert (result := part2(test_data)) == 94, f"{result=}"
assert (result := part2(test_data_2)) == 71, f"{result=}"
print("Part 2:", part2(adv.input()))
