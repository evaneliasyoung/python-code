#!/usr/bin/env python3
"""
@file      walker.py
@brief     Walks through a path.

@author    Evan Elias Young
@date      2018-01-08
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import os
import argparse

PARSER = argparse.ArgumentParser(description="Process some integers.")
PARSER.add_argument("path", metavar="path", help="The starting path")
PARSER.add_argument(
    "-s",
    default="---",
    metavar="separator",
    help="The string to prepend on directories",
)
ARGS: argparse.Namespace = PARSER.parse_args()
ARGS.path = ARGS.path[:-1] if ARGS.path.endswith("/") else ARGS.path


def get_dir_level(pth: str) -> int:
    """Will return the directory level of a path.

    Args:
        pth (string): The file's path.

    Returns:
        integer: The depth level of the file.

    """
    return len(pth.split(os.path.sep))


OUT = open(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        f"{os.path.basename(ARGS.path)}.txt",
    ),
    "w",
    encoding="utf-8",
    newline="\n",
)

OUT.write(f"Summary of {ARGS.path}/\n")
lvloff: int = get_dir_level(ARGS.path) - 1
for (root, dirs, fils) in os.walk(ARGS.path):
    lvl: int = get_dir_level(root) - lvloff
    OUT.write(f"{(lvl - 1) * ARGS.s}{root.split(os.path.sep)[-1]}\n")
    for f in fils:
        OUT.write(f"{lvl * ARGS.s}{f}\n")

OUT.close()
