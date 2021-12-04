#! /usr/bin/env python

from itertools import product
from pathlib import Path
import advent_of_code as adv

test_data = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class Board:
    def __init__(self, raw):
        self.board = [[int(line[column:column+2]) for column in range(0, 13, 3)] for line in raw.splitlines()]
        self.marked = set()

    def mark(self, draw):
        for line, column in product(range(5), range(5)):
            if self.board[line][column] == draw:
                self.marked.add((line, column))

    def is_winner(self):
        for line in range(5):
            if all((line, column) in self.marked for column in range(5)):
                return True
        for column in range(5):
            if all((line, column) in self.marked for line in range(5)):
                return True

    def score(self, draw):
        return sum(self.board[line][column] for line, column in product(range(5), range(5)) if (line, column) not in self.marked) * draw

    def __str__(self):
        return '\n'.join(' '.join(f'{cell:-2d}' for cell in line) for line in self.board)


def parse_bingo(data):
    draws, *boards = data.strip().split('\n\n')
    draws = [int(draw) for draw in draws.split(',')]
    boards = [Board(board) for board in boards]
    return draws, boards


def play(data):
    draws, boards = parse_bingo(data)
    for draw in draws:
        for board in boards:
            board.mark(draw)
            if board.is_winner():
                return board.score(draw)

assert play(test_data) == 4512

data = adv.input(Path(__file__).parent.name, str)
print("Part 1:", play(data))

def last(data):
    draws, boards = parse_bingo(data)
    for draw in draws:
        winning = []
        for board in boards:
            board.mark(draw)
            if board.is_winner():
                winning.append(board)
        for board in winning:
            if len(boards) == 1:
                return board.score(draw)
            boards.remove(board)

assert last(test_data) == 1924
print("Part 2:", last(data))
