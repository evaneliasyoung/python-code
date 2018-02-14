#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 01/08/2018
Revision : 02/10/2018
"""

import os
import argparse

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("path", metavar="path", help="The starting path")
parser.add_argument("-s", default="---", metavar="separator", help="The string to prepend on directories")
args = parser.parse_args()
args.path = args.path[:-1] if args.path.endswith("/") else args.path


def getDirLevel(pth):
    """Will return the directory level of a path.

    Args:
        pth (string): The file's path.

    Returns:
        integer: The depth level of the file.

    """
    return len(pth.split(os.path.sep))


out = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"{os.path.basename(args.path)}.txt"), "w", encoding="utf-8", newline="\n")

out.write(f"Summary of {args.path}/\n")
lvloff = getDirLevel(args.path) - 1
for (root, dirs, fils) in os.walk(args.path):
    lvl = getDirLevel(root) - lvloff
    out.write(f"{(lvl - 1) * args.s}{root.split(os.path.sep)[-1]}\n")
    [out.write(f"{lvl * args.s}{f}\n") for f in fils]

out.close()
