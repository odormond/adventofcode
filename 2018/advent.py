import requests


class Inputs:
    cookies = dict(session=open('session.cookie').read().strip())

    def __init__(self, year):
        self.base_url = f'https://adventofcode.com/{year}/day/'

    def get(self, day):
        r = requests.get(self.base_url + f'{day}/input', cookies=self.cookies)
        return r
