#!/usr/bin/env python3
"""
@file      base.py
@brief     Handles base conversion.

@author    Evan Elias Young
@date      2018-07-12
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

from string import digits, ascii_letters

base64: str = f"{digits}{ascii_letters}-_"
base85: str = f"{base64}:+.^!/*?&<>()[]{{}}@%$#"


def decode(num: str, base: str = base64) -> int:
    """Will decode a base encoded string.

    Args:
        num (string): The number base encoded.
        base (string): Base to decode from. Defaults to base64.

    Returns:
        integer: The Base10 encoded number.
    """
    max_base: int = len(base)
    rev: str = num[::-1]
    val: int = 0

    for i in enumerate(rev):
        mult: int = max_base ** i[0]
        val += base.index(rev[i[0]]) * mult
    return val


def encode(num: int, base: str = base64) -> str:
    """Will encode a base encoded string.

    Args:
        num (integer): The number to be encoded.
        base (string): Base to encode to. Defaults to base64.

    Returns:
        string: The Base encoded number.
    """
    max_base: int = len(base)
    val: str = ""

    while num > 0:
        val += base[num % max_base]
        num //= max_base
    return val[::-1]


if __name__ == "__main__":
    print("Hello Console!")

    print(encode(20000727))
    print(decode("1ci_n"))
