#!/usr/bin/env python3
"""
Author   : Evan Young
Date     : 03/31/2017
Revision : 02/10/2018
"""

import itertools as ite


def parsePunnet(mat, pat):
    """Will parse a punnet square for two genomes.

    Args:
        mat (type): Description of parameter `mat`.
        pat (type): Description of parameter `pat`.

    Returns:
        type: Description of returned object.

    """
    raw = [''.join(p) for p in ite.permutations(mat + pat, 2)]
    out = [''.join(sorted(pair, key=lambda L: (L.lower(), L))) for pair in raw]
    out.sort()
    out = [out[i * 2 + 2] for i in range(4)]
    return out


if __name__ == '__main__':
    print('Hello Console!')
    mat = input("Mother Alleles (Aa): ")
    pat = input("Father Alleles (Aa): ")
    print(parsePunnet(mat, pat))
