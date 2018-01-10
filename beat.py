#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 07/30/2016
Revision : 01/09/2018
"""

from datetime import datetime as dt

utc = dt.utcnow()
beats = utc.hour * 41.6
beats += utc.minute * 0.694
beats += utc.second * 0.011574

print(f'@{beats:.0f}')
