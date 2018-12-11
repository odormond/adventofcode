#! /usr/bin/env python3

import itertools

SERIAL_NUMBER = 8772

SIZE = 300


def cell_power(x, y, serial_number):
    rack_id = x + 10
    power = rack_id * y + serial_number
    return int(f'{power*rack_id:03d}'[-3]) - 5


cells = [[cell_power(x, y, SERIAL_NUMBER) for x in range(1, SIZE+1)] for y in range(1, SIZE+1)]


def square_power(size, step=1):
    largest = 0
    answer = -1, -1
    for x, y in itertools.product(range(0, SIZE-size+1, step), repeat=2):
        total = sum(cells[y+dy][x+dx] for dx, dy in itertools.product(range(size), repeat=2))
        if total > largest:
            largest = total
            answer = x+1, y+1
    return largest, answer


largest, (x, y) = square_power(3)
print(f"Part one: {x},{y} ({largest})")

largest = 0
for size in range(1, 31):  # SIZE+1):
    print(f"\r\033[K{size}", end='', flush=True)
    power, (x, y) = square_power(size, size)
    if power > largest:
        largest = power
        answer = x, y, size

print(f"\r\033[KWild guess: {answer} ({largest})")

x, y, size = answer
largest = 0
for size in range(size-2, size+3):
    print(f"\r\033[K{size}", end='', flush=True)
    power, (x, y) = square_power(size)
    if power > largest:
        largest = power
        answer = x, y, size

print(f"\r\033[K", end='')

x, y, size = answer
print(f"Part two: {x},{y},{size} ({largest})")
