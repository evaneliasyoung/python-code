#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 2017-07-12
Revision : 2018-07-12
"""

import tarfile
import os
from lzma import PRESET_EXTREME


def getParentDir(src):
    """Will get the directory above the given directory.

    Args:
        src (string): The directory to look above.

    Returns:
        string: The parent of the given directory.

    """
    if (src == '/'):
        par = '/'
    else:
        par = '/'.join(src.split('/')[:-1])
    par += '/'
    return par


if __name__ == '__main__':
    print('Hello Console!')
    src = input('Enter the path to the directory you are compressing (/var/www)\n')
    if (not os.path.isdir(src)):
        raise Exception('NOENT')
    src = src.replace(os.sep, '/')
    basenm = os.path.basename(src)
    par = getParentDir(src)
    os.chdir(par)

    ext = -1
    while ext not in range(3):
        ext = input('Enter the compression format\n[1] gzip\n[2] bzip2\n[3] xz\n')
        try:
            ext = int(ext) - 1
        except:
            ext = -1
    ext = ['gz', 'bz2', 'xz'][ext]

    if (ext == 'xz'):
        with tarfile.open(f'{basenm}.tar.{ext}', f'w:{ext}', preset=PRESET_EXTREME) as tar:
            tar.add(basenm)
    else:
        with tarfile.open(f'{basenm}.tar.{ext}', f'w:{ext}', compresslevel=9) as tar:
            tar.add(basenm)
