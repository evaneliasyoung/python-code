#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2016-08-26
Revision : 2020-03-08
"""

import queue
import os
import multiprocessing
import argparse
import time
from threading import Thread
from typing import List

PARSER = argparse.ArgumentParser('Linpack', description='Benchmarks the cpu')
PARSER.add_argument(
    '-t',
    '--threads',
    type=int,
    default=multiprocessing.cpu_count(),
    choices=range(1,
                  multiprocessing.cpu_count() + 1),
    help='Amount of threads to use in the test, default is max')
PARSER.add_argument('-r',
                    '--runtime',
                    type=int,
                    default=1,
                    choices=range(1, 11),
                    help='The time (in seconds) to run the test, default is 1')

ARGS = PARSER.parse_args()


def run_op() -> int:
    """ Runs one operation (three instructions).
    """
    i: int = 0
    while RUNNING:
        i += 3
    return i


if __name__ == '__main__':
    d: str = os.path.dirname(os.path.realpath(__file__))
    RUNNING: bool = True
    total: int = 0
    que: queue.Queue = queue.Queue()
    tasks: List[Thread] = [
        Thread(target=lambda q: q.put(run_op()), args=(que, ))
        for i in range(ARGS.threads)
    ]

    for t in tasks:
        t.start()

    time.sleep(ARGS.runtime)

    RUNNING = False
    time.sleep(1)

    while not que.empty():
        total += que.get()

    print(ARGS.threads)
    print(total // ARGS.runtime)
