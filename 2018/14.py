#! /usr/bin/env python3


def new_recipes(elves, board):
    return [int(d) for d in str(sum(map(int, [board[e] for e in elves])))]


n_recipes = 607331
elves = [0, 1]
board = [3, 7]
while len(board) < n_recipes + 10:
    board += new_recipes(elves, board)
    elves = [(e+1+board[e]) % len(board) for e in elves]

print("Part one:", ''.join(map(str, board[n_recipes:n_recipes+10])))


target = [6, 0, 7, 3, 3, 1]
elves = [0, 1]
board = [3, 7]
found = False
while not found:
    new = new_recipes(elves, board)
    for i in new:
        board.append(i)
        if board[-len(target):] == target:
            found = True
            break
    elves = [(e+1+board[e]) % len(board) for e in elves]

print("Part two:", len(board) - len(target))
