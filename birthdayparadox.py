#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-07-18
Revision : 2019-12-12
"""


import matplotlib.pyplot as plt
from decimal import getcontext as setprec, Decimal
from math import factorial as fct
from random import randint as rng
from typing import List


def getPerc(p: int) -> float:
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


setprec().prec = 1000
plot: bool = 0

if(plot):
    ln: int = 367
    data: List[float] = [getPerc(i) for i in range(ln)]
    x = range(ln)
    y = [d * 100 for d in data]

    fig = plt.figure()
    ax = plt.subplot2grid((1, 1), (0, 0))
    ax.grid(True, linestyle=':')
    ax.set_yticks(range(0, 101, 10))

    plt.plot(x, y)
    plt.xlabel('People')
    plt.ylabel('Percent Chance of Match')
    plt.title('Birthday Paradox')
    plt.show()


if __name__ == '__main__':
    print('Hello Console!')
    r = rng(1, 360)
    print(f'{r} People : {getPerc(r):.4%}')
