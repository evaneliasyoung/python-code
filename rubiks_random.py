#!/usr/bin/env python3
"""
@file      rubiks_random.py
@brief     Generates moves to randomize a Rubiks cube.

@author    Evan Elias Young
@date      2018-02-10
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import random


def randomize(steps: int = 20) -> list[str]:
    """Will generate a list of steps to randomize a cube.

    Args:
        steps (integer): The number of steps to list. Defaults to 20.

    Returns:
        array: The list of steps to randomize the cube.

    """
    moves: list[str] = ["R", "L", "B", "D", "F", "U"]
    que: list[str] = [random.choice(moves)]
    for _ in range(steps):
        move = que[-1]
        while move == que[-1]:
            move = random.choice(moves)
        que.append(move)
    return que


if __name__ == "__main__":
    print("Hello Console!")

    print(" ".join(randomize()))
