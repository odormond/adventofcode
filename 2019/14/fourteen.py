#! /usr/bin/env python

import advent_of_code as adv


class Reaction:
    def __init__(self, text):
        reagents, product = text.split(' => ')
        reagents = (reagent.split() for reagent in reagents.split(', '))
        cnt, self.product = product.split()
        self.cnt = int(cnt)
        self.reagents = {reagent: int(cnt) for cnt, reagent in reagents}

    def __str__(self):
        return f"{', '.join(f'{cnt} {agent}' for agent, cnt in self.reagents.items())} => {self.cnt} {self.product}"


def to_reactions(text):
    return {r.product: r for r in (Reaction(line) for line in text.splitlines())}


def find_ore(reactions, fuel=1):
    needs = {'FUEL': fuel}
    stock = {}
    while needs and set(needs) != {'ORE'}:
        product = (set(needs) - {'ORE'}).pop()
        cnt = needs.pop(product)
        if cnt >= stock.get(product, 0):
            cnt -= stock.pop(product, 0)
        else:
            stock[product] -= cnt
            continue
        reaction = reactions[product]
        if reaction.cnt <= cnt:
            copies, cnt = divmod(cnt, reaction.cnt)
            for agent, n in reaction.reagents.items():
                needs[agent] = needs.get(agent, 0) + n * copies
        if cnt:
            stock[product] = reaction.cnt - cnt
            for agent, n in reaction.reagents.items():
                needs[agent] = needs.get(agent, 0) + n
    return needs['ORE']


def find_fuel(reactions, ore):
    fuel = 1
    need_ore = find_ore(reactions, fuel)
    while need_ore < ore:
        fuel *= 2
        need_ore = find_ore(reactions, fuel)
    low_fuel = fuel // 2
    hi_fuel = fuel
    while hi_fuel - low_fuel != 1:
        mid_fuel = (low_fuel + hi_fuel) // 2
        if find_ore(reactions, mid_fuel) > ore:
            hi_fuel = mid_fuel
        else:
            low_fuel = mid_fuel
    return low_fuel


TESTS = (
    (31, None, "10 ORE => 10 A\n1 ORE => 1 B\n7 A, 1 B => 1 C\n7 A, 1 C => 1 D\n7 A, 1 D => 1 E\n7 A, 1 E => 1 FUEL"),
    (165, None, "9 ORE => 2 A\n8 ORE => 3 B\n7 ORE => 5 C\n3 A, 4 B => 1 AB\n5 B, 7 C => 1 BC\n4 C, 1 A => 1 CA\n2 AB, 3 BC, 4 CA => 1 FUEL"),
    (13312, 82892753, "157 ORE => 5 NZVS\n165 ORE => 6 DCFZ\n44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL\n12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ\n179 ORE => 7 PSHF\n177 ORE => 5 HKGWZ\n7 DCFZ, 7 PSHF => 2 XJWVT\n165 ORE => 2 GPVTF\n3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"),
    (180697, 5586022, "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG\n17 NVRVD, 3 JNWZP => 8 VPVL\n53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL\n22 VJHF, 37 MNCFX => 5 FWMGM\n139 ORE => 4 NVRVD\n144 ORE => 7 JNWZP\n5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC\n5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV\n145 ORE => 6 MNCFX\n1 NVRVD => 8 CXFTF\n1 VJHF, 6 MNCFX => 4 RFSQX\n176 ORE => 6 VJHF"),
    (2210736, 460664,"171 ORE => 8 CNZTR\n7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL\n114 ORE => 4 BHXH\n14 VRPVC => 6 BMBT\n6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL\n6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT\n15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW\n13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW\n5 BMBT => 4 WPTQ\n189 ORE => 9 KTJDG\n1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP\n12 VRPVC, 27 CNZTR => 2 XDBXC\n15 KTJDG, 12 BHXH => 5 XCVML\n3 BHXH, 2 VRPVC => 7 MZWV\n121 ORE => 7 VRPVC\n7 XCVML => 6 RJRHP\n5 BHXH, 4 VRPVC => 5 LTCX"),
)
for expected_ore_per_fuel, expected_fuel_per_trillion_ore, reactions in TESTS:
    reactions = to_reactions(reactions)
    ore = find_ore(reactions)
    assert ore == expected_ore_per_fuel, f"{ore} != {expected_or_per_fuel}"
    if expected_fuel_per_trillion_ore is not None:
        fuel = find_fuel(reactions, 1000000000000)
        assert fuel == expected_fuel_per_trillion_ore, f"{fuel} != {expected_fuel_per_trillion_ore}"

reactions = adv.input(14, to_reactions)
print("Part one:", find_ore(reactions))
print("Part two:", find_fuel(reactions, 1000000000000))
