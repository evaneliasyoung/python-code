#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-07-12
Revision : 2019-12-12
"""


import tarfile
import sys
import os
from lzma import PRESET_EXTREME
from typing import List


def compressFolder(basedir: str, basename: str) -> None:
    """Compresses a folder to a .tar.xz.

    Args:
        basedir (string): The basedir of the folder to compress.
        basename (string): The basename of the folder to compress.

    """
    os.chdir(basedir)
    with tarfile.open(f'{basename}.tar.xz', 'w:xz', preset=PRESET_EXTREME) as tar:
        tar.add(basename)


def decompressTar(basedir: str, basename: str) -> None:
    """Decompresses a .tar.xz to a folder.

    Args:
        basedir (string): The basedir of the .tar.xz to expand.
        basename (string): The basename of the .tar.xz to expand.

    """
    basename = basename.replace('.tar.xz', '')

    os.chdir(basedir)
    with tarfile.open(f'{basename}.tar.xz', 'r:xz') as tar:
        tar.extractall('.')


args: List[str] = sys.argv[1:]
if (len(args) == 0):
    raise Exception('NOENT')
else:
    path = args[0]

basedir: str = os.path.dirname(path)
basename: str = os.path.basename(path)

if (os.path.isdir(path)):
    compressFolder(basedir, basename)

if (os.path.isfile(path) and path.endswith('.tar.xz')):
    decompressTar(basedir, basename)
