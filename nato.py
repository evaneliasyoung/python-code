#!/usr/bin/env python3
"""
@file      nato.py
@brief     Translates to and from the NATO alphabet.

@author    Evan Elias Young
@date      2018-07-27
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

from string import ascii_lowercase as shorts

longs: list[str] = [
    "Alpha",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliett",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Whiskey",
    "X-ray",
    "Yankee",
    "Zulu",
]


def encode(string: str) -> str:
    """Will encode a string into NATO speak.

    Args:
        string (string): The string to encode.

    Returns:
        string: The NATO speak.

    """
    ret: list[str] = [longs[shorts.index(c)] for c in string.lower() if c in shorts]
    return " ".join(ret)


def decode(string: str) -> str:
    """Will decode NATO speak into a string.

    Args:
        string (string): The NATO speak.

    Returns:
        string: The original string.

    """
    ret: list[str] = [w[0] for w in string.split(" ")]
    return "".join(ret)


if __name__ == "__main__":
    print("Hello Console!")

    print(encode("My name is Evan"))
    print(
        decode(
            "Mike Yankee November Alpha Mike Echo India Sierra Echo Victor Alpha November"
        )
    )
