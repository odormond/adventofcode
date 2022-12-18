#! /usr/bin/env python

from itertools import chain, combinations, product

import advent_of_code as adv

test_data = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""


def fill_holes(voxels):
    (lx, hx), (ly, hy), (lz, hz) = [(min(v) - 1, max(v) + 1) for v in zip(*voxels)]
    outside = {
        p for p in chain(
            product((lx, hx), range(ly, hy+1), range(lz, hz+1)),
            product(range(lx, hx+1), (ly, hy), range(lz, hz+1)),
            product(range(lx, hx+1), range(ly, hy+1), (lz, hz)),
        )
    }
    cells = {p for p in product(range(lx, hx+1), range(ly, hy+1), range(lz, hz+1))}
    unclassified = cells - outside - voxels
    progress = True
    while progress:
        progress = False
        for x, y, z in unclassified:
            if any(
                (x+dx, y+dy, z+dz) in outside
                for dx, dy, dz in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1))
            ):
                outside.add((x, y, z))
                progress = True
        unclassified.difference_update(outside)
    return voxels | unclassified


def surface(data, filler):
    voxels = filler({tuple(map(int, line.split(','))) for line in data.splitlines()})
    sides = 6 * len(voxels)
    for p, q in combinations(voxels, 2):
        if sorted(abs(a - b) for a, b in zip(p, q)) == [0, 0, 1]:
            sides -= 2
    return sides


assert (result := surface(test_data, filler=lambda x: x)) == 64, f"{result=}"
print("Part 1:", surface(adv.input(), filler=lambda x: x))


assert (result := surface(test_data, filler=fill_holes)) == 58, f"{result=}"
print("Part 1:", surface(adv.input(), filler=fill_holes))
