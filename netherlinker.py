#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-09-19
Revision : 2020-01-08
"""


from typing import List


if __name__ == '__main__':
    overWorld1: List[str] = input('Overworld Coordinates (x,z)\n').split(',')
    underWorld1: List[str] = input('Nether Coordinates (x,z)\n').split(',')
    overWorld2: List[str] = input(
        'Desired Overworld Coordinates (x,z)\n').split(',')

    diff: List[int] = list(
        map(lambda a, b: int(b) - int(a), overWorld1, overWorld2))
    netherDiff: List[int] = list(map(lambda e: e // 8, diff))
    underWorld2: List[int] = list(
        map(lambda a, b: int(a) + int(b), underWorld1, netherDiff))

    print(
        f'\n\nMake the overworld portal at {overWorld2[0]}, y?, {overWorld2[1]}')
    print(
        f'Make the nether portal at {underWorld2[0]}, y?, {underWorld2[1]}')
