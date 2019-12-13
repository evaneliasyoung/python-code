#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-09-06
Revision : 2019-12-12
"""


import requests as req
from bs4 import BeautifulSoup as bs
from datetime import date
from dateutil.relativedelta import relativedelta as datedelta


def zeroPad(n: int) -> str:
    """Will pad a number to two digits.

    Args:
        n (integer): The number to pad.

    Returns:
        string: The zero-padded number.

    """
    if(n < 10):
        pre = '0'
    return f'{pre}{n}'


def askForPast() -> str:
    """Will ask for a past date.

    Returns:
        string: The date in url format YYYY-MM.

    """
    year: int = int(input('Year (after 1912): '))
    if(year <= 1912 or year >= date.today().year):
        exit()
    month: int = 1
    return f'{year}{zeroPad(month)}'


def getInflation(amt: float, then: str) -> float:
    """Will calculate the inflation between now and then.

    Args:
        amt (float): The amount of money to inflate.
        then (string): The past date.

    Returns:
        float: The money calculated with inflation.

    """
    d: date = date.today() - datedelta(months=2)
    now: str = f'{d.year}{zeroPad(d.month)}'
    print(
        f'https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amt}&year1={then}&year2={now}')
    res = req.get(
        f'https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amt}&year1={then}&year2={now}')
    soup = bs(res.text, 'html.parser')
    ans: str = soup.find(id='answer').string
    return float(ans)


if __name__ == '__main__':
    print('Hello Console!')
    amt: float = round(float(input('Amount: ')), 1)
    then: str = askForPast()
    print(getInflation(amt, then))
