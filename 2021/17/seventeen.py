#! /usr/bin/env python

from pathlib import Path
import advent_of_code as adv


def parse(text):
    x, y = text.split(': ')[1].strip().split(', ')
    x = x.split('=')[1].split('..')
    y = y.split('=')[1].split('..')
    x = int(x[0]), int(x[1])
    y = int(y[0]), int(y[1])
    return x, y


test_data = parse("target area: x=20..30, y=-10..-5")
data = adv.input(Path(__file__).parent.name, parse)


def tick(pos, velocity):
    x, y = pos
    vx, vy = velocity
    x += vx
    y += vy
    if vx:
        vx += 1 if vx < 0 else -1
    vy -= 1
    return (x, y), (vx, vy)


def aim_with_style(target):
    (x_low, x_hi), (y_low, y_hi) = target
    highest = 0
    highest_vx = 0
    highest_vy = 0
    hits = set()
    vx = -1
    while vx <= x_hi:
        vx += 1
        min_steps = 0
        x, y = 0, 0
        v_x, v_y = vx, 0
        while v_x > 0 and x < x_low:
            (x, y), (v_x, v_y) = tick((x, y), (v_x, v_y))
            min_steps += 1
        if x < x_low:  # Too slow to hit
            continue
        if x > x_hi:  # Too fast to hit
            continue
        # Let's start by aiming straight at the lowest target
        vy = y_low - 0
        # We will always pass by y = 0 when going down
        # so the fastest we can move and still hit is  (0 - y_low)
        while vy <= (0 - y_low):
            apex = 0
            step = 0
            x, y = 0, 0
            v_x, v_y = vx, vy
            for step in range(1, min_steps+1):
                (x, y), (v_x, v_y) = tick((x, y), (v_x, v_y))
                if y > apex:
                    apex = y
            # We're at the first x position where we can hit
            while y >= y_low:
                if x_low <= x <= x_hi and y_low <= y <= y_hi:  # hit
                    hits.add((vx, vy))
                    if apex > highest:
                        highest = apex
                        highest_vx = vx
                        highest_vy = vy
                (x, y), (v_x, v_y) = tick((x, y), (v_x, v_y))
                step += 1
                if y > apex:
                    apex = y
            vy += 1

    return len(hits), highest_vx, highest_vy, highest

assert (v := aim_with_style(test_data)) == (112, 6, 9, 45), f"Wrong v: {v}"
hits, hi_vx, hi_vy, hi = aim_with_style(data)
print("Part 1:", hi)
print("Part 2:", hits)
