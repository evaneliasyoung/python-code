#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-07-18
Revision : 2019-12-14
"""


from decimal import getcontext as setprec, Decimal
from math import factorial as fct
from typing import List


def getPerc(p: int) -> Decimal:
    """Will calculate the percent chance of matching birthdays.

    Args:
        p (integer): The amount of people.

    Returns:
        float: The percent chance of a match.

    """
    if(p > 365):
        return Decimal(1 - 0)
    fracTop: Decimal = Decimal(fct(365))
    fracBot: Decimal = Decimal((365 ** p) * fct(365 - p))

    return 1 - Decimal(fracTop / fracBot)


if __name__ == '__main__':
    from random import randint

    print('Hello Console!')

    setprec().prec = 1000
    r: int = randint(1, 360)
    print(f'{r} People : {getPerc(r):0.4%}')
