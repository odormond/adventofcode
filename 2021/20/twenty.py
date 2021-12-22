#! /usr/bin/env python

from itertools import product
from math import inf
from pathlib import Path
import advent_of_code as adv


def parse(text):
    enhancer, image = text.strip().split('\n\n')
    enhancer = [1 if pixel == '#' else 0 for pixel in enhancer]
    image = {(l, c): 1 if pixel == '#' else 0 for l, line in enumerate(image.splitlines()) for c, pixel in enumerate(line)}
    image[None] = 0
    return enhancer, image


def coverage(image):
    low_l = low_c = inf
    hi_l = hi_c = 0
    for key in image:
        if key is None:
            continue
        l, c = key
        low_l = min(low_l, l)
        low_c = min(low_c, c)
        hi_l = max(hi_l, l)
        hi_c = max(hi_c, c)
    return range(low_l-1, hi_l+2), range(low_c-1, hi_c+2)


def window_to_num(image, line, column):
    background = image[None]
    return sum(
        bit << shift
        for shift, bit in enumerate(
            reversed(
                [
                    image.get((l, c), background)
                    for l in (line - 1, line, line + 1)
                    for c in (column - 1, column, column + 1)
                ]
            )
        )
    )


def enhance_once(image, enhancer):
    enhanced_image = {(l, c): enhancer[window_to_num(image, l, c)] for l, c in product(*coverage(image))}
    enhanced_image[None] = enhancer[sum(image[None] << i for i in range(9))]
    return enhanced_image


def print_image(image):
    background = image[None]
    l_range, c_range = coverage(image)
    print('\n'.join(''.join('#' if image.get((l, c), background) else '.' for c in c_range) for l in l_range))


def enhance(image, enhancer, times):
    for i in range(times):
        image = enhance_once(image, enhancer)
    # print_image(image)
    return image


enhancer, image = parse(Path(__file__).with_name('test_data').read_text())

assert (lit := list(enhance(image, enhancer, 2).values()).count(1)) == 35, f"Wrong lit count: {lit}"
assert (lit := list(enhance(image, enhancer, 50).values()).count(1)) == 3351, f"Wrong lit count: {lit}"

enhancer, image = adv.input(Path(__file__).parent.name, parse)
print("Part 1:", list(enhance(image, enhancer, 2).values()).count(1))
print("Part 2:", list(enhance(image, enhancer, 50).values()).count(1))
