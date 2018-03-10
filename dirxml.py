#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 01/08/2018
Revision : 03/10/2018
"""

import os
from sys import platform
import argparse
from xml.sax.saxutils import quoteattr

parser = argparse.ArgumentParser(description='Tree a directory into an xml file')
parser.add_argument('path', metavar='path', help='The starting path')
parser.add_argument('-v', nargs='?', type=bool, const=True, default=False, metavar='verbose', help='Print the xml file in the terminal')
parser.add_argument('-m', nargs='?', type=bool, const=True, default=False, metavar='minify', help='Makes the xml file as small as possible')
parser.add_argument('-o', nargs='?', type=bool, const=True, default=False, metavar='open', help='Open the xml file when complete')
parser.add_argument('--folders', nargs='?', type=bool, const=True, default=False, metavar='folders', help='Only list folders')
args = parser.parse_args()
args.path = args.path[:-1] if args.path.endswith('/') or args.path.endswith('\\') else args.path

lend = '' if args.m else '\n'
lpre = '' if args.m else '  '
out = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f'{os.path.basename(args.path)}{".min" if args.m else ""}.xml'), 'w', encoding='utf-8', newline='\n')
out.write(f'<?xml version="1.0" encoding="utf-8" ?>{lend}')


def dirXML(path):
    """Will return the xml of a directory.

    Args:
        path (string): The folder's path.

    Returns:
        string: The folder's xml section.

    """
    ret = f'<dir name={quoteattr(os.path.basename(path))} permissions={quoteattr(oct(os.stat(path).st_mode & 0o0777)[-3:])}>{lend}'

    for i in os.listdir(path):
        ip = os.path.join(path, i)
        if (os.path.isdir(ip)):
            ret += lend.join([f'{lpre}{li}' for li in dirXML(os.path.join(path, i)).split('\n')[:-1]])
            ret += lend
        elif (os.path.isfile(ip) and not args.folders):
            attrs = {
                "name": i,
                "permissions": oct(os.stat(os.path.join(path, i)).st_mode & 0o0777)[-3:]
            }
            dt = 0
            if (i.startswith('.')):
                attrs['hidden'] = '1'
                dt = 1
            if (i.count('.') > dt):
                attrs['ext'] = i.split('.')[-1]

            ret += f'{lpre}<file {" ".join([f"{k}={quoteattr(attrs[k])}" for k in attrs])} />{lend}'

    ret += '</dir>\n'
    if (os.listdir(path) == []):
        ret = f'<dir name={quoteattr(os.path.basename(path))} />{lend}'
    return ret


xml = dirXML(args.path)
if (args.v):
    print(xml)
out.write(xml)
out.close()

if (args.o):
    stpre = 'start' if platform == 'win32' else 'open'
    os.system(f'{stpre} {os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.basename(args.path))}.xml')
