#! /usr/bin/env python3

from collections import namedtuple
import itertools
import os.path
import re
import advent_of_code as adv

TEST = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""

Product = namedtuple('Product', 'ingredients allergens')
PRODUCT_RE = re.compile(r'^([^(]+)(?: \(contains (.*)\))?$')


def parse_input(text):
    products = []
    for product in text.strip().splitlines():
        compounds = PRODUCT_RE.match(product)
        ingredients, allergens = compounds.groups()
        ingredients = ingredients.split()
        if allergens is not None:
            allergens = allergens.split(', ')
        products.append(Product(tuple(sorted(ingredients)), tuple(sorted(allergens))))
    return products


def disjoin(seq):
    return not any(a.intersection(b) for a, b in itertools.combinations(seq, 2))


"""
fish : -mxmxvkd  kfcds +sqjhc  nhms
       -mxmxvkd        +sqjhc        sbzzf
dairy: +mxmxvkd  kfcds  sqjhc  nhms
       +mxmxvkd                      sbzzf  trh  fvjkl
soy  :                 -sqjhc                   +fvjkl
"""


def identify_allergens(products):
    identified = {}
    all_allergens = {}
    all_ingredients = {}
    for product in products:
        for allergen in product.allergens:
            all_allergens.setdefault(allergen, set()).add(product)
        for ingredient in product.ingredients:
            all_ingredients.setdefault(ingredient, set()).add(product)
    allergens = list(all_allergens.items())
    while allergens:
        allergen, products = allergens.pop(0)
        ingredients = {p.ingredients for p in products}
        # Ingredients from the first product
        common = set(ingredients.pop())
        # Ingredients common to all the products with that allergen
        while ingredients:
            common.intersection_update(ingredients.pop())
        common = {i for i in common if i not in identified}
        if len(common) == 1:
            common = common.pop()
            identified[common] = allergen
        else:
            allergens.append((allergen, products))
    return identified, {
        ingredient: products
        for ingredient, products in all_ingredients.items()
        if ingredient not in identified
    }


products = parse_input(TEST)
allergens, safe = identify_allergens(products)
assert sum(len(products) for products in safe.values()) == 5
assert (
    ','.join(i for i, a in sorted(allergens.items(), key=lambda p: p[1])) == 'mxmxvkd,sqjhc,fvjkl'
)

data = adv.input(int(os.path.basename(os.path.dirname(__file__))), str)
products = parse_input(data)
allergens, safe = identify_allergens(products)
print("Part 1:", sum(len(products) for products in safe.values()))
print("Part 2:", ','.join(i for i, a in sorted(allergens.items(), key=lambda p: p[1])))
