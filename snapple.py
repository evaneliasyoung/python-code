#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 10/25/2017
Revision : 02/06/2018
"""

import requests as req
from bs4 import BeautifulSoup as bs
from random import choice

def getFact(fact):
   res = req.get('https://www.snapple.com/real-facts')
   soup = bs(res.text, 'html.parser')
   if (fact < 0):
      elm = choice(soup.find(id = 'fact-list').findAll('li'))
   else:
      elm = soup.find(id = 'fact-list').find(value = fact)
   return (int(elm.attrs['value']), elm.find('a').text)

if __name__ == '__main__':
   from random import randint as rng
   print('Hello Console!')
   print(getFact(-1))
