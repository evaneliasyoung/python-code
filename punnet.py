#!/usr/bin/env python3
"""
@file      punnet.py
@brief     Solves punnet squares.

@author    Evan Elias Young
@date      2017-03-31
@date      2022-02-04
@copyright Copyright 2022 Evan Elias Young. All rights reserved.
"""

import itertools as ite


def parse_punnet(mat: str, pat: str) -> list[str]:
    """Will parse a punnet square for two genomes.

    Args:
        mat (string): The mother's alleles.
        pat (string): The father's alleles.

    Returns:
        List: The mixed alleles.

    """
    raw: list[str] = ["".join(p) for p in ite.permutations(mat + pat, 2)]
    out: list[str] = [
        "".join(sorted(pair, key=lambda L: (L.lower(), L))) for pair in raw
    ]
    out.sort()
    out = [out[i * 2 + 2] for i in range(4)]
    return out


if __name__ == "__main__":
    print("Hello Console!")

    MATERNAL: str = input("Mother Alleles (Aa): ")
    PATERNAL: str = input("Father Alleles (Aa): ")
    print(parse_punnet(MATERNAL, PATERNAL))
