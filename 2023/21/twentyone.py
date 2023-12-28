#! /usr/bin/env python

from collections import defaultdict

import advent_of_code as adv

test_data = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

def parse(data):
    start = None
    rocks = set()
    for r, line in enumerate(data.splitlines()):
        for c, spot in enumerate(line):
            if spot == 'S':
                start = (r, c)
            elif spot == '#':
                rocks.add((r, c))
    return start, rocks


def part1(data, steps):
    start, rocks = parse(data)
    standing = {start}
    for step in range(steps):
        reached = set()
        while standing:
            r, c = standing.pop()
            for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                n = (r + dr, c + dc)
                if n not in rocks:
                    reached.add(n)
        standing = reached
    return len(reached)


assert (result := part1(test_data, 6)) == 16, f"{result=}"
print("Part 1:", part1(adv.input(), 64))


def part2(data, steps):
    side = len(data.splitlines())
    start, rocks = parse(data)
    standing = {start}
    block_histories = defaultdict(list)
    appearances = {}
    cyclics = defaultdict(list)
    sectors = defaultdict(list)
    for step in range(steps):
        reached = set()
        blocks = defaultdict(set)
        block_states = defaultdict(set)
        while standing:
            r, c = standing.pop()
            for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                n = (r + dr, c + dc)
                pos = (r + dr) % side, (c + dc) % side
                block = (r + dr) // side, (c + dc) // side
                if block in cyclics:
                    continue
                if pos not in rocks:
                    reached.add(n)
                    appearances.setdefault(block, step)
                    blocks[block].add((r + dr, c + dc))
                    block_states[block].add(pos)
        for block, reach in blocks.items():
            if reach in block_histories[block]:
                cyclics[block] = step
                br, bc = block
                sector = (1 if br > 0 else -1 if br < 0 else 0), (1 if bc > 0 else -1 if bc < 0 else 0)
                sectors[sector].append([sorted((y % side, x % side) for y, x in s) for s in block_histories[block]])
                reach.clear()
            else:
                block_histories[block].append(reach)
        standing = set().union(*blocks.values())
        if len(sectors) == 9:
            for sector, histories in sectors.items():
                if sector == (0, 0):
                    continue
                if len(histories) < 2 or histories[-1] != histories[-2]:
                    break
            else:
                for sector, histories in sectors.items():
                    if sector == (0, 0):
                        continue
                    while len(histories) > 1 and histories[-2] == histories[-1]:
                        del histories[-1]  # identical to the previous one
                break
    else:
        # unstable
        reached = 0
        for block, history in block_histories.items():
            if block not in cyclics:
                reached += len(history[-1])
            else:
                cycle_start = cyclics[block]
                reached += len(history[-2:][(steps - cycle_start - 1) % 2])
        return reached
    # stable
    total = 0
    for (sr, sc), histories in sectors.items():
        if (sr, sc) == (0, 0):
            # origin
            total += len(histories[-1][-2:][(steps - cyclics[(sr, sc)] - 1) % 2])
        elif 0 in (sr, sc):
            # axes
            stable_block = len(histories) * sr, len(histories) * sc
            # Contribution from the irregular blocks
            # due to the scattered rocks, it can take some time to reach the border lanes and
            # have a regular progression
            for block in range(0, len(histories) - 1):
                block = block * sr, block * sc
                total += len(block_histories[block][-2:][(steps - cyclics[block]) % 2])
            # from then we reach a new block each `side` steps
            # it takes side < len(histories[-1]) < 2*side to enter cyclic mode
            cyclic_blocks = (steps - appearances[stable_block] - len(histories[-1])) // side + 1

            # the cyclic blocks are on alternate phase but we care only for the last one when
            # we have an odd number of them
            total += cyclic_blocks // 2 * (len(histories[-1][-2]) + len(histories[-1][-1]))
            if cyclic_blocks % 2 == 1:
                total += len(histories[-1][-2:][(steps - cyclics[stable_block] - 1) % 2])
            phase = (steps - appearances[stable_block] - 1) % side
            total += len(histories[-1][phase])
            if (steps - appearances[stable_block]) // side == cyclic_blocks + 1 and phase + side < len(histories[-1]):
                # We have a second partial block that has reached `side` step fewer into the history
                total += len(histories[-1][phase + side])
        else:
            # diagonals
            # As for the axis but without the irregular block and we reach regular block from a
            # corner due to the surrounding lanes
            cyclic_blocks = (steps - appearances[(sr, sc)] - len(histories[-1])) // side + 1
            # Due to the triangular nature the diagonal sectors we have one less cyclic block in
            # each following column
            # phase = steps - appearances[(sr, sc)] - side * (cyclic_blocks - 1) - 1
            phase = (steps - appearances[(sr, sc)] - 1) % side
            for n_blocks in range(cyclic_blocks + 1):
                # the cyclic blocks are on alternate phase but we care only for the last one when
                # we have an odd number of them
                total += n_blocks // 2 * (len(histories[-1][-2]) + len(histories[-1][-1]))
                if n_blocks % 2 == 1:
                    total += len(histories[-1][-2:][(steps - cyclics[(sr, sc)] - (cyclic_blocks % 2)) % 2])
                total += len(histories[-1][phase])
                if (steps - appearances[(sr, sc)]) // side == cyclic_blocks + 1:
                    # We have a second partial block that has reached `side` step fewer into the history
                    total += len(histories[-1][phase + side])
            if (steps - appearances[(sr, sc)]) // side == cyclic_blocks + 1:
                # We have a second partial block that has reached `side` step fewer into the history
                total += len(histories[-1][phase])
    return total


for s, e in ((6, 16), (10, 50), (50, 1594), (100, 6536), (500, 167004), (1000, 668697), (5000, 16733044)):
    assert (result := part2(test_data, s)) == e, f"{result=} diff={result - s}"
print("Part 2:", part2(adv.input(), 26501365))
