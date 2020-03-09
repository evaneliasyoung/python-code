#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2018-02-10
Revision : 2020-03-08
"""

import random
from typing import List


def randomize(steps: int = 20) -> List[str]:
    """Will generate a list of steps to randomize a cube.

    Args:
        steps (integer): The number of steps to list. Defaults to 20.

    Returns:
        array: The list of steps to randomize the cube.

    """
    moves: List[str] = ['R', 'L', 'B', 'D', 'F', 'U']
    que: List[str] = [random.choice(moves)]
    for _ in range(steps):
        move = que[-1]
        while move == que[-1]:
            move = random.choice(moves)
        que.append(move)
    return que


if __name__ == '__main__':
    print('Hello Console!')

    print(' '.join(randomize()))
