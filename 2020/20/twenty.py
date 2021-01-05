#! /usr/bin/env python3

import itertools
import os.path
import advent_of_code as adv


def flip(data):
    return [row for row in reversed(data)]


def rotate(data):
    return [[row[column] for row in reversed(data)] for column in range(len(data[0]))]


class Tile:
    TOP_EDGE = 0
    LEFT_EDGE = 1
    RIGHT_EDGE = 2
    BOTTOM_EDGE = 3

    def __init__(self, text):
        header, *data = text.strip().splitlines()
        self.id = int(header[:-1].split()[1])
        self.data = [list(row) for row in data]
        self.pos = None
        self.all_border_ids = set()
        for data in (
            self.data,  # Straight
            rotate(self.data),  # 90° clockwise
            rotate(rotate(self.data)),  # 180°
            rotate(rotate(rotate(self.data))),  # 270° clockwise
        ):
            self.all_border_ids.update(
                {
                    ''.join(data[0]),  # Top border
                    ''.join(row[0] for row in data),  # Left border
                    ''.join(row[-1] for row in data),  # Right border
                    ''.join(data[-1]),  # Bottom border
                }
            )

    @property
    def border_ids(self):
        return (
            ''.join(self.data[0]),  # Top border
            ''.join(row[0] for row in self.data),  # Left border
            ''.join(row[-1] for row in self.data),  # Right border
            ''.join(self.data[-1]),  # Bottom border
        )

    def align_border(self, border_id, edge):
        for f in 'ud':
            for r in 'trbl':
                if self.border_ids[edge] == border_id:
                    return True  # is now properly aligned
                self.data = rotate(self.data)
            self.data = flip(self.data)
        return False  # Could not be aligned


def parse_input(text):
    return [Tile(tile) for tile in text.strip().split('\n\n')]


def assemble_tiles(tiles):
    tiles = tiles[:]
    pairing = {}
    for a, b in itertools.combinations(tiles, 2):
        if a.all_border_ids.intersection(b.all_border_ids):
            pairing.setdefault(a, set()).add(b)
            pairing.setdefault(b, set()).add(a)
    # Find one of the corner tile
    for corner, pairs in pairing.items():
        if len(pairs) == 2:
            right, below = pairs
            break
    # Find orientation of the corner tile
    for f in 'ud':
        for r in 'trbl':
            if right.align_border(
                corner.border_ids[Tile.RIGHT_EDGE], Tile.LEFT_EDGE
            ) and below.align_border(corner.border_ids[Tile.BOTTOM_EDGE], Tile.TOP_EDGE):
                break
            corner.data = rotate(corner.data)
        else:
            corner.data = flip(corner.data)
            continue
        break
    side = int(len(tiles) ** 0.5)
    image = [[None for x in range(side)] for y in range(side)]
    image[0][0] = corner
    for y in range(side):
        if y:
            ref = image[y - 1][0]
            border_id = ref.border_ids[Tile.BOTTOM_EDGE]
            for tile in pairing[ref]:
                if tile.align_border(border_id, Tile.TOP_EDGE):
                    image[y][0] = tile
                    break
            else:
                assert False, f"Could not find tile for (0, {y})"
        for x in range(side - 1):
            ref = image[y][x]
            border_id = ref.border_ids[Tile.RIGHT_EDGE]
            for tile in pairing[ref]:
                if tile.align_border(border_id, Tile.LEFT_EDGE):
                    image[y][x + 1] = tile
                    break
            else:
                assert False, f"Could not find tile for ({x+1}, {y})"
    return image


def corner_tiles(image):
    return image[0][0], image[0][-1], image[-1][0], image[-1][-1]


# fmt: off
"""
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
NESSY = (
    (18, 0),  # First row
    (0, 1), (5, 1), (6, 1), (11, 1), (12, 1), (17, 1), (18, 1), (19, 1),  # Second row
    (1, 2), (4, 2), (7, 2), (10, 2), (13, 2), (16, 2),  # Third row
)
# fmt: on


def stripped_monster(image):
    locations = []
    for y in range(len(image) - 3):
        for x in range(len(image[0]) - 19):
            if all(image[y + dy][x + dx] == '#' for dx, dy in NESSY):
                locations.append((x, y))
    if not locations:
        return False
    without = [row[:] for row in image]
    for x, y in locations:
        for dx, dy in NESSY:
            without[y + dy][x + dx] = '.'
    return without


def without_nessy(image_tiles):
    image = []
    for row in image_tiles:
        for y in range(1, 9):
            image.append([])
            for tile in row:
                image[-1].extend(tile.data[y][1:-1])
    for f in 'ud':
        for r in 'tlbr':
            if without := stripped_monster(image):
                return without
            image = rotate(image)
        image = flip(image)
    return []


with open(os.path.join(os.path.dirname(__file__), 'test_data')) as test:
    image = assemble_tiles(parse_input(test.read()))

checksum = 1
for tile in corner_tiles(image):
    checksum *= tile.id
assert checksum == 20899048083289
assert sum(row.count('#') for row in without_nessy(image)) == 273

tiles = adv.input(int(os.path.basename(os.path.dirname(__file__))), parse_input)
image = assemble_tiles(tiles)
checksum = 1
for tile in corner_tiles(image):
    checksum *= tile.id
print("Part 1:", checksum)
print("Part 2:", sum(row.count('#') for row in without_nessy(image)))
