#!/usr/bin/env python3
"""
@file      dirxml.py
@brief     Exports an xml listing of a path.

@author    Evan Elias Young
@date      2018-01-08
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import os
from sys import platform
import argparse
from xml.sax.saxutils import quoteattr

PARSER = argparse.ArgumentParser(description="Tree a directory into an xml file")
PARSER.add_argument("path", metavar="path", help="The starting path")
PARSER.add_argument(
    "-v",
    nargs="?",
    type=bool,
    const=True,
    default=False,
    metavar="verbose",
    help="Print the xml file in the terminal",
)
PARSER.add_argument(
    "-m",
    nargs="?",
    type=bool,
    const=True,
    default=False,
    metavar="minify",
    help="Makes the xml file as small as possible",
)
PARSER.add_argument(
    "-o",
    nargs="?",
    type=bool,
    const=True,
    default=False,
    metavar="open",
    help="Open the xml file when complete",
)
PARSER.add_argument(
    "--folders",
    nargs="?",
    type=bool,
    const=True,
    default=False,
    metavar="folders",
    help="Only list folders",
)
ARGS = PARSER.parse_args()
ARGS.path = (
    ARGS.path[:-1] if ARGS.path.endswith("/") or ARGS.path.endswith("\\") else ARGS.path
)

lend: str = "" if ARGS.m else "\n"
lpre: str = "" if ARGS.m else "  "
OUT_FILE = open(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        f'{os.path.basename(ARGS.path)}{".min" if ARGS.m else ""}.xml',
    ),
    "w",
    encoding="utf-8",
    newline="\n",
)
OUT_FILE.write(f'<?xml version="1.0" encoding="utf-8" ?>{lend}')


def dir_xml(path: str) -> str:
    """Will return the xml of a directory.

    Args:
        path (string): The folder's path.

    Returns:
        string: The folder's xml section.

    """
    ret: str = f"<dir name={quoteattr(os.path.basename(path))} "
    ret += f"permissions={quoteattr(oct(os.stat(path).st_mode & 0o0777)[-3:])}>{lend}"

    for i in os.listdir(path):
        item_path = os.path.join(path, i)
        if os.path.isdir(item_path):
            ret += lend.join(
                [
                    f"{lpre}{li}"
                    for li in dir_xml(os.path.join(path, i)).split("\n")[:-1]
                ]
            )
            ret += lend
        elif os.path.isfile(item_path) and not ARGS.folders:
            attrs = {
                "name": i,
                "permissions": oct(os.stat(os.path.join(path, i)).st_mode & 0o0777)[
                    -3:
                ],
            }
            dir_trace = 0
            if i.startswith("."):
                attrs["hidden"] = "1"
                dir_trace = 1
            if i.count(".") > dir_trace:
                attrs["ext"] = i.split(".")[-1]

            ret += f'{lpre}<file {" ".join([f"{k}={quoteattr(attrs[k])}" for k in attrs])} />{lend}'

    ret += "</dir>\n"
    if os.listdir(path) == []:
        ret = f"<dir name={quoteattr(os.path.basename(path))} />{lend}"
    return ret


xml: str = dir_xml(ARGS.path)
if ARGS.v:
    print(xml)
OUT_FILE.write(xml)
OUT_FILE.close()

if ARGS.o:
    stpre: str = "start" if platform == "win32" else "open"
    cmd: str = f"{stpre} "
    cmd += os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.basename(ARGS.path)
    )
    cmd += ".xml"
    os.system(cmd)
