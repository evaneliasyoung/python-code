#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 07/30/2016
Revision : 02/10/2018
"""

from datetime import datetime as dt


def __init__():
    utc = dt.utcnow()
    beats = utc.hour * 41.6
    beats += utc.minute * 0.694
    beats += utc.second * 0.011574
    return beats


if __name__ == '__main__':
    print('Hello Console!')
    print(f'@{__init__():.0f}')
