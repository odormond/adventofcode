#! /usr/bin/env python

import advent_of_code as adv


WIDTH = 25
HEIGHT = 6


data = adv.input(8, lambda data: [int(d) for d in data.strip()])
layers = [data[start:start+WIDTH*HEIGHT] for start in range(0, len(data), WIDTH*HEIGHT)]
_, l_id, layer = min((layer.count(0), l, layer) for l, layer in enumerate(layers))

print("Part one:", layer.count(1) * layer.count(2))


RENDER = ' #'

image = []
for i in range(WIDTH*HEIGHT):
    for layer in layers:
        if layer[i] != 2:
            image.append(RENDER[layer[i]])
            break
    else:
        image.append(None)

assert None not in image
print("Part two:")
for l in range(HEIGHT):
    print(''.join(image[l*WIDTH:(l+1)*WIDTH]))
