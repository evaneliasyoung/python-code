#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2018-07-27
Revision : 2018-09-13
"""

from string import ascii_lowercase as shorts
longs = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot',
         'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima',
         'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo',
         'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey',
         'X-ray', 'Yankee', 'Zulu']


def encode(s):
    """Will encode a string into NATO speak.

    Args:
        s (string): The string to encode.

    Returns:
        string: The NATO speak.

    """
    ret = [longs[shorts.index(c)] for c in s.lower() if c in shorts]
    return ' '.join(ret)


def decode(s):
    """Will decode NATO speak into a string.

    Args:
        s (string): The NATO speak.

    Returns:
        string: The original string.

    """
    ret = [w[0] for w in s.split(' ')]
    return ''.join(ret)


if __name__ == '__main__':
    print('Hello Console!')
    print(encode('My name is Evan'))
    print(decode('Mike Yankee November Alpha Mike Echo India Sierra Echo Victor Alpha November'))
