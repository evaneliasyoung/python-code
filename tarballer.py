#!/usr/bin/env python3
"""
@file      tarballer.py
@brief     Compresses a directory into a tarball.

@author    Evan Elias Young
@date      2017-07-12
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import tarfile
import sys
import os
from lzma import PRESET_EXTREME


def compress_folder(directory: str, name: str) -> None:
    """Compresses a folder to a .tar.xz.

    Args:
        directory (string): The directory of the folder to compress.
        name (string): The name of the folder to compress.

    """
    os.chdir(directory)
    with tarfile.open(f"{name}.tar.xz", "w:xz", preset=PRESET_EXTREME) as tar:
        tar.add(name)


def decompress_tar(directory: str, name: str) -> None:
    """Decompresses a .tar.xz to a folder.

    Args:
        directory (string): The directory of the .tar.xz to expand.
        name (string): The name of the .tar.xz to expand.

    """
    name = name.replace(".tar.xz", "")

    os.chdir(directory)
    with tarfile.open(f"{name}.tar.xz", "r:xz") as tar:
        tar.extractall(".")


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    if len(args) != 0:
        path: str = args[0]
    else:
        raise Exception("NOENT")

    base_dir: str = os.path.dirname(path)
    base_name: str = os.path.basename(path)

    if os.path.isdir(path):
        compress_folder(base_dir, base_name)

    if os.path.isfile(path) and path.endswith(".tar.xz"):
        decompress_tar(base_dir, base_name)
