from pathlib import Path

import requests


BASE_URL = "https://adventofcode.com/2021/day/"
with (Path(__file__).parents[1] / "session.cookie").open() as cookie:
    COOKIES = dict(session=cookie.read().strip())


def input(day, converter):
    cache = Path('data.txt')
    if cache.exists():
        with cache.open() as cache:
            return converter(cache.read())
    else:
        with cache.open('w') as cache:
            data = requests.get(BASE_URL + f"{day}/input", cookies=COOKIES).text
            cache.write(data)
        return converter(data)


def to_list_of_int(text):
    text = text.strip()
    return [int(i) for i in (text.split(",") if "," in text else text.splitlines())]


def to_list_of_str(text):
    return text.splitlines()
