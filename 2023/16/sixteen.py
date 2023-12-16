#! /usr/bin/env python

import advent_of_code as adv

test_data = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".strip()

def parse(data):
    return data.splitlines()


def energize(grid, input_beam):
    height = len(grid)
    width = len(grid[0])
    energized = [[0] * width for _ in range(height)]
    beams = [input_beam]
    while beams:
        x, y, dirs = beams.pop(0)
        if dirs == 1 and x + 1 < width:  # rightward beam
            cell = grid[y][x+1]
            if cell in '.-' and energized[y][x+1] & 1 == 0:
                energized[y][x+1] |= 1
                beams.append((x+1, y, 1))
            if cell == '|':
                if energized[y][x+1] & 8 == 0:
                    energized[y][x+1] |= 8
                    beams.append((x+1, y, 8))
                if energized[y][x+1] & 4 == 0:
                    energized[y][x+1] |= 4
                    beams.append((x+1, y, 4))
            if cell == '/':
                if energized[y][x+1] & 8 == 0:
                    energized[y][x+1] |= 8
                    beams.append((x+1, y, 8))
            if cell == '\\':
                if energized[y][x+1] & 4 == 0:
                    energized[y][x+1] |= 4
                    beams.append((x+1, y, 4))
        if dirs == 2 and x > 0:  # leftward beam
            cell = grid[y][x-1]
            if cell in '.-' and energized[y][x-1] & 2 == 0:
                energized[y][x-1] |= 2
                beams.append((x-1, y, 2))
            if cell == '|':
                if energized[y][x-1] & 8 == 0:
                    energized[y][x-1] |= 8
                    beams.append((x-1, y, 8))
                if energized[y][x-1] & 4 == 0:
                    energized[y][x-1] |= 4
                    beams.append((x-1, y, 4))
            if cell == '/':
                if energized[y][x-1] & 4 == 0:
                    energized[y][x-1] |= 4
                    beams.append((x-1, y, 4))
            if cell == '\\':
                if energized[y][x-1] & 8 == 0:
                    energized[y][x-1] |= 8
                    beams.append((x-1, y, 8))
        if dirs == 4 and y + 1 < height:  # downward beam
            cell = grid[y+1][x]
            if cell in '.|' and energized[y+1][x] & 4 == 0:
                energized[y+1][x] |= 4
                beams.append((x, y+1, 4))
            if cell == '-':
                if energized[y+1][x] & 2 == 0:
                    energized[y+1][x] |= 2
                    beams.append((x, y+1, 2))
                if energized[y+1][x] & 1 == 0:
                    energized[y+1][x] |= 1
                    beams.append((x, y+1, 1))
            if cell == '/':
                if energized[y+1][x] & 2 == 0:
                    energized[y+1][x] |= 2
                    beams.append((x, y+1, 2))
            if cell == '\\':
                if energized[y+1][x] & 1 == 0:
                    energized[y+1][x] |= 1
                    beams.append((x, y+1, 1))
        if dirs == 8 and y > 0:  # upward beam
            cell = grid[y-1][x]
            if cell in '.|' and energized[y-1][x] & 8 == 0:
                energized[y-1][x] |= 8
                beams.append((x, y-1, 8))
            if cell == '-':
                if energized[y-1][x] & 2 == 0:
                    energized[y-1][x] |= 2
                    beams.append((x, y-1, 2))
                if energized[y-1][x] & 1 == 0:
                    energized[y-1][x] |= 1
                    beams.append((x, y-1, 1))
            if cell == '/':
                if energized[y-1][x] & 1 == 0:
                    energized[y-1][x] |= 1
                    beams.append((x, y-1, 1))
            if cell == '\\':
                if energized[y-1][x] & 2 == 0:
                    energized[y-1][x] |= 2
                    beams.append((x, y-1, 2))
    return sum(1 if e else 0 for line in energized for e in line)


def part1(data):
    grid = parse(data)
    return energize(grid, (-1, 0, 1))


assert (result := part1(test_data)) == 46, f"{result=}"
print("Part 1:", part1(adv.input()))


def part2(data):
    grid = parse(data)
    height = len(grid)
    width = len(grid[0])
    return max(
        max(energize(grid, (-1, y, 1)) for y in range(height)),
        max(energize(grid, (width, y, 2)) for y in range(height)),
        max(energize(grid, (x, -1, 4)) for x in range(width)),
        max(energize(grid, (x, height, 8)) for x in range(width)),
    )


assert (result := part2(test_data)) == 51, f"{result=}"
print("Part 2:", part2(adv.input()))
