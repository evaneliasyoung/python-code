#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 11/04/2017
Revision : 01/21/2018
"""

import webbrowser as web
from copy import deepcopy as copy

def openBrowsers(raw,st = 'Missouri'):
   full = raw.title().split(' ')
   short = copy(full)
   if(len(short) == 3): short.remove(short[1])

   url = [
      f'https://www.spokeo.com/{"-".join(short)}/{st}',
      f'https://www.truepeoplesearch.com/results?name={"%20".join(full)}&citystatezip={st}',
      f'https://www.intelius.com/people-search/{"-".join(full)}/{st}',
      f'https://www.whitepages.com/name/{"-".join(full)}/{st}/'
   ]

   for u in url: web.open(u)

if __name__ == '__main__':
   print('Hello Console!')
   openBrowsers(input('Name: '))
