#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2016-07-30
Revision : 2020-03-08
"""

from datetime import datetime as dt


def __init__() -> float:
    utc: dt = dt.utcnow()
    beats: float = utc.hour * 41.6
    beats += utc.minute * 0.694
    beats += utc.second * 0.011574
    return beats


if __name__ == '__main__':
    print('Hello Console!')

    print(f'@{__init__():.0f}')
