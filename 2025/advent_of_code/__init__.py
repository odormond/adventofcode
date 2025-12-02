import sys
from pathlib import Path

import requests

TIMEOUT = 30
BASE_URL = "https://adventofcode.com/2025/day/"
with (Path(__file__).parents[1] / "session.cookie").open() as cookie:
    COOKIES = {"session": cookie.read().strip()}


NUMBERS = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
    "twenty", "twentyone", "twentytwo", "twentythree", "twentyfour", "twentyfive", "twentysix", "twentyseven", "twentyeight", "twentynine",  # noqa: E501
    "thirty", "thirtyone",
]
SKELETON = """#! /usr/bin/env python

import advent_of_code as aoc

test_data = \"""\\
\"""

def parse(data):
    return data


def part1(data):
    return parse(data)


assert (result := part1(test_data)) == "", f"{result=}"
print("Part 1:", part1(aoc.input()))


def part2(data):
    return parse(data)


assert (result := part2(test_data)) == "", f"{result=}"
print("Part 2:", part2(aoc.input()))
"""


def setup():
    if len(sys.argv) == 2:
        base_dir = Path(sys.argv[1])
    else:
        base_dir = Path()
    for day in range(1, 26):
        day_dir = base_dir / str(day)
        day_dir.mkdir()
        day_script = (day_dir / NUMBERS[day]).with_suffix(".py")
        day_script.write_text(SKELETON)
        day_script.chmod(0o755)


def run_day():
    if "--pdb" in sys.argv:
        pdb = ["-m", "pdb", "-c", "cont"]
        del sys.argv[sys.argv.index("--pdb")]
    else:
        pdb = []
    day = sys.argv[1]
    import os
    os.chdir(day)
    os.execv(sys.executable, [sys.executable, *pdb, f"{NUMBERS[int(day)]}.py", *sys.argv[2:]])  # noqa: S606


def input(converter=str):  # noqa: A001
    day = Path(sys.argv[0]).resolve().parent.name
    cache = Path("data.txt")
    if cache.exists():
        with cache.open() as cache:
            return converter(cache.read())
    else:
        with cache.open("w") as cache:
            data = requests.get(BASE_URL + f"{day}/input", cookies=COOKIES, timeout=TIMEOUT).text
            cache.write(data)
        return converter(data)


def to_list_of_int(text):
    text = text.strip()
    return [int(i) for i in (text.split(",") if "," in text else text.splitlines())]


def to_list_of_str(text):
    return text.splitlines()
