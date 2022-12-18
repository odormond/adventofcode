#! /usr/bin/env python

from itertools import product

import advent_of_code as adv

test_data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

WIDTH = 7
START_FROM_LEFT = 2
START_FROM_TOP = 4

PIECES = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},  # -
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},  # +
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},  # ┘
    {(0, 0), (0, 1), (0, 2), (0, 3)},  # |
    {(0, 0), (1, 0), (0, 1), (1, 1)},  # ■
]
N_PIECES = len(PIECES)


def rotate(lst):
    lst[:] = lst[1:] + lst[:1]
    return lst


def shift(piece, dx, dy):
    moved_piece = {(x + dx, y + dy) for x, y in piece}
    if any(x < 0 or x >= WIDTH for x, _ in moved_piece):
        return piece
    return moved_piece


def tetris(pushes, rocks):
    pushes = list(pushes)
    pieces = PIECES[:]
    top = 0
    tower = {(x, top) for x in range(WIDTH)}
    piece_cnt = 0
    prev_top = top
    repetitions = {}
    jumped = False
    piece = None
    while rocks:
        if piece is None:
            piece = shift(rotate(pieces)[-1], START_FROM_LEFT, START_FROM_TOP + top)
            piece_cnt += 1
        push = rotate(pushes)[-1]

        moved_piece = shift(piece, {'<': -1, '>': 1}[push], 0)
        if not tower.intersection(moved_piece):
            piece = moved_piece

        moved_piece = shift(piece, 0, -1)
        if tower.intersection(moved_piece):
            tower |= piece
            piece = None
            rocks -= 1
            top = max(y for x, y in tower)
            if not jumped and piece_cnt % N_PIECES == 0:
                # Let's see if we can find the same last N_PIECES laid out identically before.
                # Before we put the last N_PIECES to rest, the tower reached prev_top. So we'll
                # look for an identical configuration of the [top, prev_top) section below prev_top.
                for old_top in range(prev_top, 0, -1):
                    if not any(
                        ((x, top - dy) in tower) ^ ((x, old_top - dy) in tower)
                        for x, dy in product(range(WIDTH), range(top - prev_top))
                    ):
                        # We've found an identical lay out at `old_top` but it might be a coincidence.
                        # If it's really the cyclic part of the tower then it will repeat further:
                        # top     old top   ground
                        #  v         v        v
                        #  A----B----C--------|
                        #  >----<
                        #     L = repeat_length
                        # When top was at B, we recorded a repeat starting at C and with length L after
                        # laying out N pieces.
                        # Now that top is at A and we have laid out M pieces, we first recorded (B, L) = M
                        # because (B, L//2) is unknown, then we check if (C, L) is known and if (B, L) was
                        # actually recorded after the same number of pieces were put to rest.
                        # This last check is required because we don't actually record in the repetitions
                        # which tower pattern repeats but only after how many pieces it occurred.
                        # Every N_PIECES we get a pattern and any pattern will repeat. We just stop at the
                        # first time we have one that repeat twice.
                        repeat_length = (top - old_top) // 2
                        if (
                            (old_top, repeat_length) in repetitions
                            and repetitions.get((old_top + repeat_length, repeat_length)) == piece_cnt
                        ):
                            phase = repetitions[(old_top, repeat_length)] * 2 - piece_cnt
                            wave_length = piece_cnt - repetitions[(old_top, repeat_length)]
                            jump, rocks = divmod(rocks, wave_length)
                            tower = {(x, y + jump * repeat_length) for x, y in tower}
                            top = max(y for x, y in tower)
                            jumped = True
                            break
                        repetitions[(old_top, top - old_top)] = piece_cnt
                prev_top = top
        else:
            piece = moved_piece
    return top


assert (result := tetris(test_data, 2022)) == 3068, f"{result=}"
print("Part 1:", tetris(adv.input(str.strip), 2022))

assert (result := tetris(test_data, 1000000000000)) == 1514285714288, f"{result=}"
print("Part 2:", tetris(adv.input(str.strip), 1000000000000))
