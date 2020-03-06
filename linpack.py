#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2016-08-26
Revision : 2020-01-08
"""

import queue
import os
import multiprocessing
import argparse
import time
from threading import Thread
import time
from typing import List


parser = argparse.ArgumentParser('Linpack', description='Benchmarks the cpu')
parser.add_argument('-t', '--threads', type=int, default=multiprocessing.cpu_count(),
                    choices=range(1, multiprocessing.cpu_count()+1), help='Amount of threads to use in the test, default is max')
parser.add_argument('-r', '--runtime', type=int, default=1,
                    choices=range(1, 11), help='The time (in seconds) to run the test, default is 1')

args = parser.parse_args()


def op() -> int:
    """ Runs one operation (three instructions).
    """
    i: int = 0
    while running:
        i += 3
    return i


if __name__ == '__main__':
    d: str = os.path.dirname(os.path.realpath(__file__))
    running: bool = True
    total: int = 0
    que: queue.Queue = queue.Queue()
    tasks: List[Thread] = [Thread(target=lambda q: q.put(
        op()), args=(que,)) for i in range(args.threads)]

    [t.start() for t in tasks]

    time.sleep(args.runtime)

    running = False
    time.sleep(1)

    while not que.empty():
        total += que.get()

    print(args.threads)
    print(total // args.runtime)
