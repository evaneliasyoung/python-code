#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-09-06
Revision : 2018-09-13
"""

import requests as req
from bs4 import BeautifulSoup as bs
from datetime import date
from dateutil.relativedelta import relativedelta as datedelta


def zeroPad(n):
    """Will pad a number to two digits.

    Args:
        n (integer): The number to pad.

    Returns:
        string: The zero-padded number.

    """
    if(n < 10):
        pre = '0'
    return f'{pre}{n}'


def askForPast():
    """Will ask for a past date.

    Returns:
        string: The date in url format YYYY-MM.

    """
    year = int(input('Year (after 1912): '))
    if(year <= 1912 or year >= date.today().year):
        exit()
    month = 1
    return f'{year}{zeroPad(month)}'


def getInflation(amt, then):
    """Will calculate the inflation between now and then.

    Args:
        amt (float): The amount of money to inflate.
        then (string): The past date.

    Returns:
        float: The money calculated with inflation.

    """
    d = date.today() - datedelta(months=2)
    now = f'{d.year}{zeroPad(d.month)}'
    print(f'https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amt}&year1={then}&year2={now}')
    res = req.get(f'https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amt}&year1={then}&year2={now}')
    soup = bs(res.text, 'html.parser')
    ans = soup.find(id='answer').string
    return ans


if __name__ == '__main__':
    print('Hello Console!')
    amt = round(float(input('Amount: ')), 1)
    then = askForPast()
    print(getInflation(amt, then))
