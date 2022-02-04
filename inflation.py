#!/usr/bin/env python3
"""
@file      inflation.py
@brief     Calculates US inflation.

@author    Evan Elias Young
@date      2017-09-06
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import sys
from datetime import date
import requests as req
from bs4 import BeautifulSoup as bs
from dateutil.relativedelta import relativedelta as datedelta


def ask_for_past() -> str:
    """Will ask for a past date.

    Returns:
        string: The date in url format YYYY-MM.

    """
    year: int = int(input("Year (after 1912): "))
    if year <= 1912 or year >= date.today().year:
        sys.exit()
    month: int = 1
    return f"{year}{month:0>2}"


def get_inflation(amount: float, past: str) -> float:
    """Will calculate the inflation between now and then.

    Args:
        amount (float): The amount of money to inflate.
        past (string): The past date.

    Returns:
        float: The money calculated with inflation.

    """
    cur_date: date = date.today() - datedelta(months=2)
    now: str = f"{cur_date.year}{cur_date.month:0>2}"
    res = req.get(
        f"https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amount}&year1={past}&year2={now}"
    )
    soup = bs(res.text, "html.parser")
    ans: str = soup.find(id="answer").string
    return float(ans[1:].replace(",", ""))


if __name__ == "__main__":
    from random import randint

    print("Hello Console!")

    amt: float = randint(0, 1000) + (randint(0, 99) / 100)
    cur_year: int = date.today().year
    yr: int = randint(1913, cur_year - 1)
    then: str = f"{yr}01"
    print(f"{yr} -> {cur_year}")
    print(f"${amt:0.2f} -> ${get_inflation(amt, then):0.2f}")
