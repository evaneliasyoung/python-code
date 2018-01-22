#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 08/12/2015
Revision : 01/21/2018
"""

# <region> Modules
import argparse
import random
import os
from string import ascii_letters as asciiLetters
# </region>

# <region> Variables
key = []
chars = []
# </region>

# <region> Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-n', help = 'Enables the use of numbers in the key', action = 'store_true')
parser.add_argument('-l', help = 'Enables the use of letters in the key', action = 'store_true')
parser.add_argument('-c', help = 'Enables the use of other characters in the key', action = 'store_true')
parser.add_argument('-le', metavar = 'N', help = 'Changes the key\'s length, default is 16', type = int, default = 16)
parser.add_argument('-o', help = 'Outputs key to the scripts location, rather than to the console', action = 'store_true')
args = parser.parse_args()

if args.o:
   out_path = os.path.dirname(os.path.abspath(__file__))

if args.n: chars.extend(range(10))
if args.l: chars.extend([c for c in asciiLetters])
if args.c: chars.extend(['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', '{', ']', '}', '\\', ';', ':', '\'', '"', ',', '<', '.', '>', '/', '?'])

if not args.n and not args.l and not args.c:
   chars.extend(other)
# </region>

# <region> Main
for i in range(args.le):
   key.append(random.choice(chars))

if (args.o):
   with open('ket.txt', 'w') as f:
      f.write(''.join(key))
else:
   print(''.join(key))
# </region>
