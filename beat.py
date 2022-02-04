#!/usr/bin/env python3
"""
@file      beat.py
@brief     Claculates internet beat time.

@author    Evan Elias Young
@date      2016-07-30
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

from datetime import datetime as dt


def __init__() -> float:
    utc: dt = dt.utcnow()
    beats: float = utc.hour * 41.6
    beats += utc.minute * 0.694
    beats += utc.second * 0.011574
    return beats


if __name__ == "__main__":
    print("Hello Console!")

    print(f"@{__init__():.0f}")
