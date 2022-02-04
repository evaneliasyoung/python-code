#!/usr/bin/env python3
"""
@file      keygen.py
@brief     Generates random keystrings.

@author    Evan Elias Young
@date      2015-08-12
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import argparse
import random
from string import ascii_letters as asciiLetters
from typing import List

key: List[str] = []
chars: List[str] = []

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    "-n", help="Enables the use of numbers in the key", action="store_true"
)
PARSER.add_argument(
    "-l", help="Enables the use of letters in the key", action="store_true"
)
PARSER.add_argument(
    "-c", help="Enables the use of other characters in the key", action="store_true"
)
PARSER.add_argument(
    "-le",
    metavar="N",
    help="Changes the key's length, default is 16",
    type=int,
    default=16,
)
PARSER.add_argument(
    "-o",
    help="Outputs key to the scripts location, rather than to the console",
    action="store_true",
)
ARGS = PARSER.parse_args()

if ARGS.n:
    chars.extend([str(i) for i in range(10)])
if ARGS.l:
    chars.extend(asciiLetters)
if ARGS.c:
    chars.extend(
        [
            "~",
            "`",
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "=",
            "+",
            "[",
            "{",
            "]",
            "}",
            "\\",
            ";",
            ":",
            "'",
            '"',
            ",",
            "<",
            ".",
            ">",
            "/",
            "?",
        ]
    )

if not ARGS.n and not ARGS.l and not ARGS.c:
    chars.extend(asciiLetters)
    chars.extend([str(i) for i in range(10)])

KEY: str = "".join([random.choice(chars) for i in range(ARGS.le)])

if ARGS.o:
    open("key.txt", "w").write(KEY)
else:
    print(KEY)
