#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 07/27/2015
Revision : 01/21/2018
"""

from string import ascii_lowercase as shorts
longs = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot',
         'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima',
         'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo',
         'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey',
         'X-ray', 'Yankee', 'Zulu']

def encode(s):
   ret = [longs[shorts.index(c)] for c in s.lower() if c in shorts]
   return ' '.join(ret)
   
def decode(s):
   ret = ''
   for w in s.split(' '):
      ret += w[0]
   return ret

if __name__ == '__main__':
   print('Hello Console!')
   print(encode('My name is evan'))
   print(decode('Mike Yankee November Alpha Mike Echo India Sierra Echo Victor Alpha November'))
