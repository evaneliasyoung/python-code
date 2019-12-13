#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2018-07-12
Revision : 2019-12-12
"""


from string import digits, ascii_letters
base64: str = f'{digits}{ascii_letters}-_'
base85: str = f'{base64}:+.^!/*?&<>()[]{{}}@%$#'


def decode(num: str, base: str = base64) -> int:
    """Will decode a base encoded string.

    Args:
        num (string): The number base encoded.
        base (string): Base to decode from. Defaults to base64.

    Returns:
        integer: The Base10 encoded number.

    """
    mx: int = len(base)
    rev: str = num[::-1]
    val: int = 0

    for i in range(0, len(rev)):
        mult: int = mx ** i
        val += base.index(rev[i]) * mult
    return val


def encode(num: int, base: str = base64) -> str:
    """Will encode a base encoded string.

    Args:
        num (integer): The number to be encoded.
        base (string): Base to encode to. Defaults to base64.

    Returns:
        string: The Base encoded number.

    """
    mx: int = len(base)
    val: str = ''

    while(num > 0):
        val += base[num % mx]
        num //= mx
    return val[::-1]


if __name__ == '__main__':
    print('Hello Console!')
    print(encode(20000727))
    print(decode('1ci_n'))
