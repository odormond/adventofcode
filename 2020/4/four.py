#! /usr/bin/env python3

import os.path
import re
import advent_of_code as adv


COLOR_RE = re.compile(r"^#[0-9a-f]{6}$")
PID_RE = re.compile(r"^\d{9}$")

REQ_FIELDS = {
    "byr",  # (Birth Year)
    "iyr",  # (Issue Year)
    "eyr",  # (Expiration Year)
    "hgt",  # (Height)
    "hcl",  # (Hair Color)
    "ecl",  # (Eye Color)
    "pid",  # (Passport ID)
}

FIELDS = REQ_FIELDS.union({"cid"})  # (Country ID)


def to_list_of_passport(text):
    return [
        dict(field.split(":", 1) for field in raw.split()) for raw in text.strip().split("\n\n")
    ]


TEST_BATCH = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""


def is_valid(passport):
    return REQ_FIELDS.intersection(passport) == REQ_FIELDS


assert len(list(filter(is_valid, to_list_of_passport(TEST_BATCH)))) == 2

passports = adv.input(int(os.path.basename(os.path.dirname(__file__))), to_list_of_passport)
print("Part 1:", len(list(filter(is_valid, passports))))

"""
byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
"""


def is_year_in_range(year, low, hi):
    try:
        return len(year) == 4 and low <= int(year) <= hi
    except ValueError:
        return False


def valid_byr(passport):
    return is_year_in_range(passport["byr"], 1920, 2002)


def valid_iyr(passport):
    return is_year_in_range(passport["iyr"], 2010, 2020)


def valid_eyr(passport):
    return is_year_in_range(passport["eyr"], 2020, 2030)


def valid_hgt(passport):
    hgt = passport["hgt"]
    measure, unit = hgt[:-2], hgt[-2:]
    if unit not in ("cm", "in"):
        return False
    try:
        measure = int(measure)
    except ValueError:
        return False
    low, hi = {"cm": (150, 193), "in": (59, 76)}[unit]
    return low <= measure <= hi


def valid_hcl(passport):
    return COLOR_RE.match(passport["hcl"]) is not None


def valid_ecl(passport):
    return passport["ecl"] in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def valid_pid(passport):
    return PID_RE.match(passport["pid"]) is not None


def is_really_valid(passport):
    for check in (
        is_valid,
        valid_byr,
        valid_iyr,
        valid_eyr,
        valid_hgt,
        valid_hcl,
        valid_ecl,
        valid_pid,
    ):
        if not check(passport):
            return False
    return True


TEST_INVALID = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""
assert len(list(filter(is_really_valid, to_list_of_passport(TEST_INVALID)))) == 0

TEST_VALID = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""
assert len(list(filter(is_really_valid, to_list_of_passport(TEST_VALID)))) == 4

print("Part 2:", len(list(filter(is_really_valid, passports))))
