#!/usr/bin/env python3
"""
@file      person.py
@brief     Scours the internet for PII.

@author    Evan Elias Young
@date      2017-11-04
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import webbrowser as web
from copy import deepcopy as copy


def open_browsers(raw: str, state: str = "Missouri") -> None:
    """Will open the browser to the correct sites.

    Args:
        raw (string): The person's name.
        state (string): The state of residence. Defaults to 'Missouri'.

    """
    full: list[str] = raw.title().split(" ")
    short: list[str] = copy(full)
    if len(short) == 3:
        short.remove(short[1])

    urls: list[str] = [
        f'https://www.spokeo.com/{"-".join(short)}/{state}',
        f'https://www.truepeoplesearch.com/results?name={"%20".join(full)}&citystatezip={state}',
        f'https://www.intelius.com/people-search/{"-".join(full)}/{state}',
        f'https://www.whitepages.com/name/{"-".join(full)}/{state}/',
    ]

    for url in urls:
        web.open(url)


if __name__ == "__main__":
    print("Hello Console!")
    open_browsers(input("Name: "))
