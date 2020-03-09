#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2017-03-31
Revision : 2020-03-08
"""

import itertools as ite
from typing import List


def parse_punnet(mat: str, pat: str) -> List[str]:
    """Will parse a punnet square for two genomes.

    Args:
        mat (string): The mother's alleles.
        pat (string): The father's alleles.

    Returns:
        List: The mixed alleles.

    """
    raw: List[str] = [''.join(p) for p in ite.permutations(mat + pat, 2)]
    out: List[str] = [
        ''.join(sorted(pair, key=lambda L: (L.lower(), L))) for pair in raw
    ]
    out.sort()
    out = [out[i * 2 + 2] for i in range(4)]
    return out


if __name__ == '__main__':
    print('Hello Console!')

    MATERNAL: str = input('Mother Alleles (Aa): ')
    PATERNAL: str = input('Father Alleles (Aa): ')
    print(parse_punnet(MATERNAL, PATERNAL))
