#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-10-25
Revision : 2020-03-08
"""

from random import choice
from typing import Tuple
import requests as req
from bs4 import BeautifulSoup as bs


def get_fact(fact: int = -1) -> Tuple[int, str]:
    """Will fetch a fact from a fact number.

    Args:
        fact {int}: The number of the fact. (default: {-1})

    Returns:
        Tuple[int, str] -- The fact number and the fact.
    """
    res: req.Response = req.get('https://www.snapple.com/real-facts')
    soup: bs = bs(res.text, 'html.parser')
    if fact < 0:
        elm = choice(soup.find(id='fact-list').findAll('li'))
    else:
        elm = soup.find(id='fact-list').find(value=fact)
    return (int(elm.attrs['value']), elm.find('a').text)


if __name__ == '__main__':
    print('Hello Console!')

    print(get_fact())
