#! /usr/bin/env python

from functools import reduce
from pathlib import Path
import advent_of_code as adv


def parse_bits(bits):
    version, bits = int(bits[:3], 2), bits[3:]
    type_id, bits = int(bits[:3], 2), bits[3:]
    if type_id == 4:
        raw = ''
        cont = 1
        while cont:
            cont, chunk, bits = int(bits[:1], 2), bits[1:5], bits[5:]
            raw += chunk
        value = int(raw, 2)
    else:
        length_type, bits = int(bits[:1], 2), bits[1:]
        if length_type == 0:
            length, bits = int(bits[:15], 2), bits[15:]
            raw, bits = bits[:length], bits[length:]
            value = []
            while raw:
                packet, raw = parse_bits(raw)
                value.append(packet)
        else:
            count, bits = int(bits[:11], 2), bits[11:]
            value = []
            for i in range(count):
                packet, bits = parse_bits(bits)
                value.append(packet)

    return (version, type_id, value), bits


def parse(text):
    n_bits = len(text.strip()) * 4
    bits = bin(int(text, 16))[2:]
    bits = '0' * (n_bits - len(bits)) + bits
    result = parse_bits(bits)
    return result


def versions_sum(packet):
    version, type_id, value = packet
    if type_id != 4:
        return sum(versions_sum(p) for p in value) + version
    return version


assert parse("D2FE28") == ((6, 4, 2021), '000')
assert parse("38006F45291200") == ((1, 6, [(6, 4, 10), (2, 4, 20)]), '0000000')
assert parse("EE00D40C823060") == ((7, 3, [(2, 4, 1), (4, 4, 2), (1, 4, 3)]), '00000')
assert versions_sum(parse("8A004A801A8002F478")[0]) == 16
assert versions_sum(parse("620080001611562C8802118E34")[0]) == 12
assert versions_sum(parse("C0015000016115A2E0802F182340")[0]) == 23
assert versions_sum(parse("A0016C880162017C3686B18A3D4780")[0]) == 31

packet, rest = adv.input(Path(__file__).parent.name, parse)
print("Part 1:", versions_sum(packet))


def evaluate(packet):
    version, type_id, value = packet
    match type_id:
        case 0:
            return sum(map(evaluate, value))
        case 1:
            return reduce(lambda a, b: a * b, map(evaluate, value), 1)
        case 2:
            return min(map(evaluate, value))
        case 3:
            return max(map(evaluate, value))
        case 4:
            return value
        case 5:
            return 1 if evaluate(value[0]) > evaluate(value[1]) else 0
        case 6:
            return 1 if evaluate(value[0]) < evaluate(value[1]) else 0
        case 7:
            return 1 if evaluate(value[0]) == evaluate(value[1]) else 0
    raise ValueError(f"Unknown operation: {type_id}")


assert evaluate(parse("C200B40A82")[0]) == 3
assert evaluate(parse("04005AC33890")[0]) == 54
assert evaluate(parse("880086C3E88112")[0]) == 7
assert evaluate(parse("CE00C43D881120")[0]) == 9
assert evaluate(parse("D8005AC2A8F0")[0]) == 1
assert evaluate(parse("F600BC2D8F")[0]) == 0
assert evaluate(parse("9C005AC2F8F0")[0]) == 0
assert evaluate(parse("9C0141080250320F1802104A08")[0]) == 1
print("Part 2:", evaluate(packet))
