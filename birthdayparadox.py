#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 07/18/2017
Revision : 01/21/2018
"""

import matplotlib.pyplot as plt
from decimal import getcontext as setprec, Decimal as dec
from math import factorial as fct
from random import randint as rng

def getPerc(p):
   if(p > 365): return dec(1 - 0)
   fracTop = dec(fct(365))
   fracBot = dec((365 ** p) * fct(365 - p))

   return 1 - dec(fracTop / fracBot)

setprec().prec = 1000
plot = 0

if(plot):
   ln = 366+1
   data = [getPerc(i) for i in range(ln)]
   x = range(ln)
   y = [d*100 for d in data]

   fig = plt.figure()
   ax = plt.subplot2grid((1,1),(0,0))
   ax.grid(True, linestyle=":")
   ax.set_yticks(range(0, 101, 10))

   plt.plot(x, y)
   plt.xlabel("People")
   plt.ylabel("Percent Chance of Match")
   plt.title("Birthday Paradox")
   plt.show()

if __name__ == '__main__':
   print('Hello Console!')
   r = rng(1, 360)
   print(f'{r} People : {getPerc(r):.4%}')
