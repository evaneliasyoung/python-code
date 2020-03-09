#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-07-18
Revision : 2020-03-08
"""

from decimal import getcontext as setprec, Decimal
from math import factorial as fct


def get_percent(ppl: int) -> Decimal:
    """Will calculate the percent chance of matching birthdays.

    Args:
        ppl (integer): The amount of people.

    Returns:
        float: The percent chance of a match.

    """
    if ppl > 365:
        return Decimal(1 - 0)
    frac_top: Decimal = Decimal(fct(365))
    frac_bot: Decimal = Decimal((365**ppl) * fct(365 - ppl))

    return 1 - Decimal(frac_top / frac_bot)


if __name__ == '__main__':
    from random import randint

    print('Hello Console!')

    setprec().prec = 1000
    r: int = randint(1, 360)
    print(f'{r} People : {get_percent(r):0.4%}')
