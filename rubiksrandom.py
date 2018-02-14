#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 02/10/2018
Revision : 02/10/2018
"""

import random


def randomize(steps=20):
    """Will generate a list of steps to randomize a cube.

    Args:
        steps (integer): The number of steps to list. Defaults to 20.

    Returns:
        array: The list of steps to randomize the cube.

    """
    moves = ['R', 'L', 'B', 'D', 'F', 'U']
    que = [random.choice(moves)]
    for i in range(steps):
        mv = que[-1]
        while mv == que[-1]:
            mv = random.choice(moves)
        que.append(mv)
    return que


if __name__ == '__main__':
    print('Hello Console!')
    print(' '.join(randomize()))
