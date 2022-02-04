#!/usr/bin/env python3
"""
@file      holiday.py
@brief     Reads holidays from a website.

@author    Evan Elias Young
@date      2018-03-01
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

from calendar import month_name as months, monthrange as mran
import re
from datetime import datetime as dt, timedelta
import requests as req
from bs4 import BeautifulSoup as bs

now: dt = dt.now()
mon: str = months[now.month].lower()
fut: dt = now + timedelta(6)

url: str = f"http://www.holidayinsights.com/moreholidays/{mon}.htm"
RES = req.get(url)
SOUP = bs(RES.text, "html.parser")
DATA = SOUP.select(
    "body > p:nth-of-type(1) > table:nth-of-type(2) > tr > td:nth-of-type(2)"
)[0]
raw: str = DATA.decode()

MATCH = re.search(r"<ul>.*<hr/>\n<br/>", raw, re.DOTALL)
if not MATCH:
    exit(1)
SOUP = bs(raw[MATCH.start() : MATCH.end()], "html.parser")
ALL_LINKS = SOUP.select("p > a")[0].parent.decode()
DAYS: list[str] = ALL_LINKS.replace("</p>", "").replace("\n", "").split("<p>")
DAYS = [d.strip() for d in DAYS]

evnts: list[list[str]] = []
for i in range(32):
    evnts.append([])
for d in DAYS:
    if re.search("\\d+", d):
        e: str = re.sub("\\d+.", "", d)
        e = re.sub("</a>.*", "", e)
        e = re.sub("<[^>]*>", "", e)
        e = re.sub("\\s{2,}", " ", e)
        evnts[int(d[:2])].append(e)

if __name__ == "__main__":
    print("Hello Console!")

    for i in range(
        now.day, fut.day if now.month == fut.month else mran(now.year, now.month)[1]
    ):
        print(i, evnts[i])
