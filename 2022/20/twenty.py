#! /usr/bin/env python

import advent_of_code as adv

test_data = adv.to_list_of_int("""\
1
2
-3
3
-2
0
4
""")

data = adv.input(adv.to_list_of_int)

DECRYPTION_KEY = 811589153

def mix(data, key, rounds):
    data = [d * key for d in data]
    l = len(data)
    initial_pos = list(range(l))
    for round_ in range(1, rounds + 1):
        for to_move in range(l):
            idx = initial_pos.index(to_move)
            data = data[idx:] + data[:idx]
            initial_pos = initial_pos[idx:] + initial_pos[:idx]
            m = data.pop(0)
            i = initial_pos.pop(0)
            if m > 0:
                pos = m % (l - 1)
            elif m < 0:
                pos = -(-m % (l - 1))
            else:
                pos = 0
            data.insert(pos, m)
            initial_pos.insert(pos, i)
    return data


def grove_coordinate(data, decryption_key, rounds):
    data = mix(data, decryption_key, rounds)
    pos = data.index(0)
    data = data[pos:] + data[:pos]
    l = len(data)
    return data[1000 % l], data[2000 % l], data[3000 % l]


assert (result := sum(grove_coordinate(test_data, 1, 1))) == 3, f"{result=}"
print("Part 1:", sum(grove_coordinate(data, 1, 1)))


assert (result := sum(grove_coordinate(test_data, DECRYPTION_KEY, 10))) == 1623178306, f"{result=}"
print("Part 2:", sum(grove_coordinate(data, DECRYPTION_KEY, 10)))
