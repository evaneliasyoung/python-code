#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 2018-07-12
Revision : 2018-07-12
"""
from string import digits, ascii_letters
base64 = f'{digits}{ascii_letters}-_'
base85 = f'{base64}:+.^!/*?&<>()[]{{}}@%$#'


def decode(num, base=base64):
    """Will decode a base encoded string.

    Args:
        num (string): The number base encoded.
        base (string): Base to decode from. Defaults to base64.

    Returns:
        integer: The Base10 encoded number.

    """
    mx = len(base)
    rev = num[::-1]
    val = 0

    for i in range(0, len(rev)):
        mult = mx**i
        val += base.index(rev[i])*mult
    return val


def encode(num, base=base64):
    """Will encode a base encoded string.

    Args:
        num (string): The number to be encoded.
        base (string): Base to encode to. Defaults to base64.

    Returns:
        integer: The Base encoded number.

    """
    mx = len(base)
    val = ""
    while(num > 0):
        val += base[num % mx]
        num //= mx
    return val[::-1]
