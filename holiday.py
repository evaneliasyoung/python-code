#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 03/01/2018
Revision : 03/01/2018
"""

import requests as req
from calendar import month_name as months, monthrange as mran
from datetime import datetime as dt, timedelta
from bs4 import BeautifulSoup as bs
import re


now = dt.now()
mon = months[now.month].lower()
fut = now + timedelta(6)

url = f'http://www.holidayinsights.com/moreholidays/{mon}.htm'
res = req.get(url)
soup = bs(res.text, 'html.parser')
data = soup.select('body > p:nth-of-type(1) > table:nth-of-type(2) > tr > td:nth-of-type(2)')[0]
raw = data.decode()

mtch = re.search(r'<ul>.*<hr/>\n<br/>', raw, re.DOTALL)
soup = bs(raw[mtch.start():mtch.end()], 'html.parser')
alls = soup.select('p > a')[0].parent.decode()
days = alls.replace('</p>', '').replace('\n', '').split('<p>')
days = [d.strip() for d in days]

evnts = []
for i in range(32):
    evnts.append([])
for d in days:
    if(re.search('\d+', d)):
        e = re.sub('\d+.', '', d)
        e = re.sub('</a>.*', '', e)
        e = re.sub('<[^>]*>', '', e)
        e = re.sub('\s{2,}', ' ', e)
        evnts[int(d[:2])].append(e)

if __name__ == '__main__':
    print('Hello Console!')
    for i in range(now.day, fut.day if now.month == fut.month else mran(now.year, now.month)[1]):
        print(i, evnts[i])
