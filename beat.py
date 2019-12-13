#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2016-07-30
Revision : 2019-12-12
"""


from datetime import datetime as dt


def __init__() -> float:
    """Will return the current time in the beat standard.

    """
    utc: dt = dt.utcnow()
    beats: float = utc.hour * 41.6
    beats += utc.minute * 0.694
    beats += utc.second * 0.011574
    return beats


if __name__ == '__main__':
    print('Hello Console!')
    print(f'@{__init__():.0f}')
