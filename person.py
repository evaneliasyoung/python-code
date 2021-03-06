#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-11-04
Revision : 2020-03-08
"""

import webbrowser as web
from copy import deepcopy as copy
from typing import List


def open_browsers(raw: str, state: str = 'Missouri') -> None:
    """Will open the browser to the correct sites.

    Args:
        raw (string): The person's name.
        state (string): The state of residence. Defaults to 'Missouri'.

    """
    full: List[str] = raw.title().split(' ')
    short: List[str] = copy(full)
    if len(short) == 3:
        short.remove(short[1])

    urls: List[str] = [
        f'https://www.spokeo.com/{"-".join(short)}/{state}',
        f'https://www.truepeoplesearch.com/results?name={"%20".join(full)}&citystatezip={state}',
        f'https://www.intelius.com/people-search/{"-".join(full)}/{state}',
        f'https://www.whitepages.com/name/{"-".join(full)}/{state}/'
    ]

    for url in urls:
        web.open(url)


if __name__ == '__main__':
    print('Hello Console!')
    open_browsers(input('Name: '))
