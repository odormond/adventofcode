#! /usr/bin/env python

from itertools import combinations, permutations, product
from pathlib import Path
import numpy as np
import advent_of_code as adv


def to_beacons_scans(text):
    return [
        [
            tuple(int(pos) for pos in beacon.split(','))
            for beacon in scanner.splitlines()[1:]
        ]
        for scanner in text.strip().split('\n\n')
    ]


test_scans = to_beacons_scans(Path(__file__).with_name('test_data').read_text())
scans = adv.input(Path(__file__).parent.name, to_beacons_scans)


def vectorized(scanner):
    vectors = {}
    for a, b in combinations(scanner, 2):
        na, nb = np.array(a), np.array(b)
        vector = na - nb
        length = vector @ vector
        assert length not in vectors
        vectors[length] = (a, b)
    return vectors


TRANSFORMATIONS = [
    np.array(swap) * np.array(flip)
    for swap, flip in product(
        permutations(((1, 0, 0), (0, 1, 0), (0, 0, 1)), 3),
        product((1, -1), (1, -1), (1, -1)),
    )
]


class UnAlignableError(Exception):
    pass


def align_pair(scanner_a, scanner_b):
    delta_a = vectorized(scanner_a)
    delta_b = vectorized(scanner_b)
    common = set(delta_a).intersection(set(delta_b))
    delta_a = {d: p for d, p in delta_a.items() if d in common}
    delta_b = {d: p for d, p in delta_b.items() if d in common}
    common_a = set()
    common_b = set()
    for d in common:
        a, b = delta_a[d]
        common_a.add(a)
        common_a.add(b)
        a, b = delta_b[d]
        common_b.add(a)
        common_b.add(b)
    if len(common_b) < 12:
        raise UnAlignableError(f"Too small overlap: {len(common_b)}")

    matches = set()
    unique_a = {}
    discards = set()
    for l0, l1 in combinations(common, 2):
        pa = set(delta_a[l0]).intersection(delta_a[l1])
        pb = set(delta_b[l0]).intersection(delta_b[l1])
        if pa and pb:
            a, b = match = (pa.pop(), pb.pop())
            if a in unique_a and b != unique_a[a]:
                discards.update({match, (a, unique_a[a])})
            else:
                unique_a[a] = b
            if match not in matches:
                matches.add(match)
            matches.add(match)
            assert not pa
            assert not pb
    matches = list(matches - discards)

    # Identify transformation
    vectors_a, vectors_b = [], []
    for (a0, b0), (a1, b1) in combinations(matches, 2):
        vectors_a.append(np.array(a1) - np.array(a0))
        vectors_b.append(np.array(b1) - np.array(b0))
    for transform in TRANSFORMATIONS:
        if all((va == transform @ vb).all() for va, vb in zip(vectors_a, vectors_b)):
            break
    else:
        assert False, "Could not identify transformation"

    # Identify offset
    a0, b0 = matches[0]
    offset = tuple(np.array(a0) - transform @ np.array(b0))
    assert all(tuple(np.array(a) - transform @ np.array(b)) == offset for a, b in matches[1:]), f"Wrong offset: {offset}"
    return offset, transform


offset_1_0, transform_1_0 = align_pair(test_scans[0], test_scans[1])
assert offset_1_0 == (68, -1246, -43)
offset_4_1, transform_4_1 = align_pair(test_scans[1], test_scans[4])
offset_4_0 = tuple(np.array((68, -1246, -43)) + transform_1_0 @ np.array(offset_4_1))
assert offset_4_0 == (-20, -1133, 1061)


def align(scans):
    alignments = {}
    alignable = set()
    for a, b in combinations(range(len(scans)), 2):
        try:
            offset, transform = align_pair(scans[a], scans[b])
        except UnAlignableError:
            continue
        alignments.setdefault(a, []).append((b, offset, transform))
        alignments.setdefault(b, []).append((a, *align_pair(scans[b], scans[a])))
        alignable.add(a)
        alignable.add(b)
    scanners = [(0, 0, 0)]
    all_beacons = set(scans[0])
    aligned = alignments.pop(0)
    while aligned:
        target, offset, transform = aligned.pop(0)
        scanners.append(offset)
        for beacon in scans[target]:
            all_beacons.add(tuple(transform @ np.array(beacon) + np.array(offset)))
        if target in alignments:
            aligned.extend(
                [
                    (
                        remote,
                        tuple(transform @ np.array(r_offset) + np.array(offset)),
                        transform @ r_transform,
                    )
                    for remote, r_offset, r_transform in alignments.pop(target)
                ]
            )
    assert len(alignable) == len(scans), f"Unalignable scans: {sorted(set(range(len(scans))) - alignable)}"
    return all_beacons, scanners


def farthest(scanners):
    return max(abs(x1-x0 + y1-y0 + z1-z0) for (x0, y0, z0), (x1, y1, z1) in combinations(scanners, 2))


beacons, scanners = align(test_scans)
assert beacons == {
    (-892, 524, 684),
    (-876, 649, 763),
    (-838, 591, 734),
    (-789, 900, -551),
    (-739, -1745, 668),
    (-706, -3180, -659),
    (-697, -3072, -689),
    (-689, 845, -530),
    (-687, -1600, 576),
    (-661, -816, -575),
    (-654, -3158, -753),
    (-635, -1737, 486),
    (-631, -672, 1502),
    (-624, -1620, 1868),
    (-620, -3212, 371),
    (-618, -824, -621),
    (-612, -1695, 1788),
    (-601, -1648, -643),
    (-584, 868, -557),
    (-537, -823, -458),
    (-532, -1715, 1894),
    (-518, -1681, -600),
    (-499, -1607, -770),
    (-485, -357, 347),
    (-470, -3283, 303),
    (-456, -621, 1527),
    (-447, -329, 318),
    (-430, -3130, 366),
    (-413, -627, 1469),
    (-345, -311, 381),
    (-36, -1284, 1171),
    (-27, -1108, -65),
    (7, -33, -71),
    (12, -2351, -103),
    (26, -1119, 1091),
    (346, -2985, 342),
    (366, -3059, 397),
    (377, -2827, 367),
    (390, -675, -793),
    (396, -1931, -563),
    (404, -588, -901),
    (408, -1815, 803),
    (423, -701, 434),
    (432, -2009, 850),
    (443, 580, 662),
    (455, 729, 728),
    (456, -540, 1869),
    (459, -707, 401),
    (465, -695, 1988),
    (474, 580, 667),
    (496, -1584, 1900),
    (497, -1838, -617),
    (527, -524, 1933),
    (528, -643, 409),
    (534, -1912, 768),
    (544, -627, -890),
    (553, 345, -567),
    (564, 392, -477),
    (568, -2007, -577),
    (605, -1665, 1952),
    (612, -1593, 1893),
    (630, 319, -379),
    (686, -3108, -505),
    (776, -3184, -501),
    (846, -3110, -434),
    (1135, -1161, 1235),
    (1243, -1093, 1063),
    (1660, -552, 429),
    (1693, -557, 386),
    (1735, -437, 1738),
    (1749, -1800, 1813),
    (1772, -405, 1572),
    (1776, -675, 371),
    (1779, -442, 1789),
    (1780, -1548, 337),
    (1786, -1538, 337),
    (1847, -1591, 415),
    (1889, -1729, 1762),
    (1994, -1805, 1792),
}
assert farthest(scanners) == 3621
beacons, scanners = align(scans)
print("Part 1:", len(beacons))
print("Part 2:", farthest(scanners))
