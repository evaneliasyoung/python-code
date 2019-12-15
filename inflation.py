#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-09-06
Revision : 2019-12-14
"""


import requests as req
from bs4 import BeautifulSoup as bs
from datetime import date
from dateutil.relativedelta import relativedelta as datedelta


def askForPast() -> str:
    """Will ask for a past date.

    Returns:
        string: The date in url format YYYY-MM.

    """
    year: int = int(input('Year (after 1912): '))
    if year <= 1912 or year >= date.today().year:
        exit()
    month: int = 1
    return f'{year}{month:0>2}'


def getInflation(amt: float, then: str) -> float:
    """Will calculate the inflation between now and then.

    Args:
        amt (float): The amount of money to inflate.
        then (string): The past date.

    Returns:
        float: The money calculated with inflation.

    """
    d: date = date.today() - datedelta(months=2)
    now: str = f'{d.year}{d.month:0>2}'
    res = req.get(
        f'https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amt}&year1={then}&year2={now}')
    soup = bs(res.text, 'html.parser')
    ans: str = soup.find(id='answer').string
    return float(ans[1:].replace(',', ''))


if __name__ == '__main__':
    from random import randint

    print('Hello Console!')

    amt: float = randint(0, 1000) + (randint(0, 99) / 100)
    now: int = date.today().year
    yr: int = randint(1913, now - 1)
    then: str = f'{yr}01'
    print(f'{yr} -> {now}')
    print(f'${amt:0.2f} -> ${getInflation(amt, then):0.2f}')
