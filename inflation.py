#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 09/06/2017
Revision : 01/21/2018
"""

import requests as req
from bs4 import BeautifulSoup as bs
from datetime import date
from dateutil.relativedelta import relativedelta as datedelta

def zeroPad(n):
   if(n < 10):
      return f'0{n}'
   return n
def askForPast():
   mnl = ['january', 'feburary', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
   year = int(input('Year (after 1912): '))
   if(year <= 1912 or year >= date.today().year):
      exit()
   month = 1
   return f'{year}{zeroPad(month)}'
def getInflation(amt, then):
   d = date.today() - datedelta(months = 2)
   now = f'{d.year}{zeroPad(d.month)}'
   print(f'https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amt}&year1={then}&year2={now}')
   res = req.get(f'https://data.bls.gov/cgi-bin/cpicalc.pl?cost1={amt}&year1={then}&year2={now}')
   soup = bs(res.text, 'html.parser')
   ans = soup.find(id='answer').string
   return ans

if __name__ == '__main__':
   print('Hello Console!')
   amt = round(float(input('Amount: ')),1)
   then = askForPast()
   print(getInflation(amt, then))
