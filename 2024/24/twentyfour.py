#! /usr/bin/env python

from contextlib import suppress
import re

import advent_of_code as aoc

test_data = """\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

test_data_2 = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""


GATE_RE = re.compile(r"(\S+) (AND|OR|XOR) (\S+) -> (\S+)")


def order(gate):
    a, op, b, out = gate
    if a < b:
        return gate
    return b, op, a, out


def parse(data):
    inputs, raw_gates = data.split("\n\n")
    wires = (wire.split(": ") for wire in inputs.splitlines())
    inputs = {wire: value == "1" for wire, value in wires}
    gates = [order(GATE_RE.match(gate).groups()) for gate in raw_gates.splitlines()]
    return inputs, gates


def compute(inputs, gates):
    gates = gates.copy()
    wires = inputs.copy()
    while gates:
        a, op, b, out = gates.pop(0)
        if a in wires and b in wires:
            a = wires[a]
            b = wires[b]
            match op:
                case "AND":
                    wires[out] = a and b
                case "OR":
                    wires[out] = a or b
                case "XOR":
                    wires[out] = a ^ b
        else:
            gates.append((a, op, b, out))
    outputs = {wire: value for wire, value in wires.items() if wire[0] == "z"}
    return sum(int(value) * 2**int(wire[1:]) for wire, value in outputs.items())


def part1(data):
    inputs, gates = parse(data)
    return compute(inputs, gates)



assert (result := part1(test_data)) == 4, f"{result=}"
assert (result := part1(test_data_2)) == 2024, f"{result=}"
print("Part 1:", part1(aoc.input()))

"""
x y z zz
0 0 0 0
0 1 1 0
1 0 1 0
1 1 0 1
z = x ^ y
zz = x * y

c x y  z cz    x*y  x+y  c*(x+y)  x*y + c*(x+y)  c*x c*y  c*x + c*y  c * x^y  x*y + c*(x^y)
0 0 0  0 0      0    0     0          0           0   0       0          0        0
0 0 1  1 0      0    1     0          0           0   0       0          0        0
0 1 0  1 0      0    1     0          0           0   0       0          0        0
0 1 1  0 1      1    1     0          1           0   0       0          0        1
1 0 0  1 0      0    0     0          0           0   0       0          0        0
1 0 1  0 1      0    1     1          1           0   1       1          1        1
1 1 0  0 1      0    1     1          1           1   0       1          1        1
1 1 1  1 1      1    1     1          1           1   1       1          0        1
z = x ^ y ^ c
cz = x*y + c*(x+y) = x*y + c*(x^y) = x*y + c*x + c*y
                     +-- used ---+
"""

def id_bit(a, b, out):
    bits = []
    for v in (a, b, out):
        with suppress(ValueError):
            bits.append(int(v[-2:]))
    return max(bits)


def part2(data):
    inputs, gates = parse(data)
    n_bits = len(inputs) // 2
    assert all(a[1:] == b[1:] for a, op, b, out in gates if a[0] == "x" and b[0] == "y")
    renames = {f"z{n_bits:02d}": f"carry{n_bits-1:02d}"}
    all_renames = {**renames}
    for a, op, b, out in gates:
        if (a, op , b) == ("x00", "AND", "y00"):
            assert out not in all_renames
            all_renames[out] = renames[out] = "carry00"
        elif a[0] == "x" and b[0] == "y" and out[0] != "z":
            all_renames[out] = renames[out] = op + a[1:]
    gates = [(renames.get(a, a), op, renames.get(b, b), renames.get(out, out)) for a, op, b, out in gates]
    while True:
        renames = {}
        for a, op, b, out in gates:
            if any(out.startswith(prefix) for prefix in ("carry", "XOR", "OR", "AND")):
                continue  # already renamed
            a, b = sorted([a, b])
            if op == "AND" and (a.startswith("carry") or b.startswith("carry")) and not out.startswith("z"):
                assert b[0] not in "xy"
                assert a.startswith("XOR") or a.startswith("AND")
                assert out not in all_renames
                all_renames[out] = renames[out] = "carry" + a
            elif op == "OR" and a.startswith("AND") and b.startswith("carry") and not out.startswith("z"):
                assert out not in all_renames
                all_renames[out] = renames[out] = "carry" + a[-2:]
            elif out[0] == "z" and a.startswith("XOR") and not b.startswith("carry"):
                assert b not in all_renames
                all_renames[b] = renames[b] = f"carry{int(out[1:]) - 1:02d}"
        if not renames:
            break
        gates = [(renames.get(a, a), op, renames.get(b, b), renames.get(out, out)) for a, op, b, out in gates]
    bits = [[] for _ in range(n_bits)]
    for a, op, b, out in sorted(gates, key=lambda v: (v[-1][-2:], v[-1][:-2])):
        a, b = sorted([a, b])
        bits[id_bit(a, b, out)].append((op, a, b, out))
    swapped = set()
    for bit_ops in bits[1:]:
        match sorted(bit_ops):
            case [
                ("AND", xor_n1, carry_m1, carry_tmp1),
                ("AND", x1, y1, and_n1),
                ("OR", and_n2, carry_tmp2, carry_n),
                ("XOR", xor_n2, carry_m2, z),
                ("XOR", x2, y2, xor_n3)
            ]:
                if (
                    x1[0] == "x" and y1[0] == "y" and z[0] == "z"
                    and x1 == x2
                    and y1 == y2
                    and and_n1 == and_n2
                    and xor_n1 == xor_n2 == xor_n3
                    and carry_m1 == carry_m2
                    and carry_tmp1 == carry_tmp2
                ):
                    continue  # Wired correctly

                swap = set()
                # Check outputs
                if not carry_tmp1.startswith("carry"):
                    swap.add(carry_tmp1)
                if not and_n1.startswith("AND"):
                    swap.add(and_n1)
                if not carry_n.startswith("carry"):
                    swap.add(carry_n)
                if not z.startswith("z"):
                    swap.add(z)
                if not xor_n3.startswith("XOR"):
                    swap.add(xor_n3)
                if not swap:
                    # Check inputs
                    if not xor_n1.startswith("XOR"):
                        swap.add(xor_n1)
                    if not carry_m1.startswith("carry"):
                        swap.add(carry_m1)
                    if not and_n2.startswith("AND"):
                        swap.add(and_n2)
                    if not carry_tmp2.startswith("carry"):
                        swap.add(carry_tmp2)
                    if not xor_n2.startswith("XOR"):
                        swap.add(xor_n2)
                    if not carry_m2.startswith("carry"):
                        swap.add(carry_m2)
                swapped |= swap

            case _:
                print("Unexpected sequence of bit ops:")
                for op, a, b, out in sorted(bit_ops):
                    print("\t", a, op, b, "->", out)
                raise SystemExit(1)

    reversed_renames = {v: k for k, v in all_renames.items()}
    return ",".join(sorted(reversed_renames.get(wire, wire) for wire in swapped))


print("Part 2:", part2(aoc.input()))
