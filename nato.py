#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2018-07-27
Revision : 2020-03-08
"""

from string import ascii_lowercase as shorts
from typing import List

longs: List[str] = [
    'Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel',
    'India', 'Juliett', 'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa',
    'Quebec', 'Romeo', 'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey',
    'X-ray', 'Yankee', 'Zulu'
]


def encode(string: str) -> str:
    """Will encode a string into NATO speak.

    Args:
        string (string): The string to encode.

    Returns:
        string: The NATO speak.

    """
    ret: List[str] = [
        longs[shorts.index(c)] for c in string.lower() if c in shorts
    ]
    return ' '.join(ret)


def decode(string: str) -> str:
    """Will decode NATO speak into a string.

    Args:
        string (string): The NATO speak.

    Returns:
        string: The original string.

    """
    ret: List[str] = [w[0] for w in string.split(' ')]
    return ''.join(ret)


if __name__ == '__main__':
    print('Hello Console!')

    print(encode('My name is Evan'))
    print(
        decode(
            'Mike Yankee November Alpha Mike Echo India Sierra Echo Victor Alpha November'
        ))
