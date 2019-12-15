#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-11-04
Revision : 2019-12-14
"""


import webbrowser as web
from copy import deepcopy as copy
from typing import List


def openBrowsers(raw: str, st: str = 'Missouri') -> None:
    """Will open the browser to the correct sites.

    Args:
        raw (string): The person's name.
        st (string): The state of residence. Defaults to 'Missouri'.

    """
    full: List[str] = raw.title().split(' ')
    short: List[str] = copy(full)
    if(len(short) == 3):
        short.remove(short[1])

    url: List[str] = [
        f'https://www.spokeo.com/{"-".join(short)}/{st}',
        f'https://www.truepeoplesearch.com/results?name={"%20".join(full)}&citystatezip={st}',
        f'https://www.intelius.com/people-search/{"-".join(full)}/{st}',
        f'https://www.whitepages.com/name/{"-".join(full)}/{st}/'
    ]

    for u in url:
        web.open(u)


if __name__ == '__main__':
    print('Hello Console!')
    openBrowsers(input('Name: '))
