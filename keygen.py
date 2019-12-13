#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2015-08-12
Revision : 2019-12-12
"""


import argparse
import random
import os
from string import ascii_letters as asciiLetters
from typing import List


key: List[str] = []
chars: List[str] = []


parser = argparse.ArgumentParser()
parser.add_argument(
    '-n', help='Enables the use of numbers in the key', action='store_true')
parser.add_argument(
    '-l', help='Enables the use of letters in the key', action='store_true')
parser.add_argument(
    '-c', help='Enables the use of other characters in the key', action='store_true')
parser.add_argument('-le', metavar='N',
                    help='Changes the key\'s length, default is 16', type=int, default=16)
parser.add_argument(
    '-o', help='Outputs key to the scripts location, rather than to the console', action='store_true')
args = parser.parse_args()

if args.o:
    out_path = os.path.dirname(os.path.abspath(__file__))

if args.n:
    chars.extend([str(i) for i in range(10)])
if args.l:
    chars.extend(asciiLetters)
if args.c:
    chars.extend(['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=',
                  '+', '[', '{', ']', '}', '\\', ';', ':', '\'', '"', ',', '<', '.', '>', '/', '?'])

if not args.n and not args.l and not args.c:
    chars.extend(asciiLetters)
    chars.extend([str(i) for i in range(10)])

key = [random.choice(chars) for i in range(args.le)]

if (args.o):
    open('key.txt', 'w').write(''.join(key))
else:
    print(''.join(key))
