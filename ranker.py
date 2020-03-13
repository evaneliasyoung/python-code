#!/usr/bin/env python3
"""
Author   : Evan Elias Young
Date     : 2020-03-13
Revision : 2020-03-13
"""

from typing import List


def get_total_rounds(num_options: int) -> int:
    """Determines the total rounds of ratings.

    Arguments:
        num_options {int} -- The number of options.

    Returns:
        int -- The number of rounds.
    """
    return sum(range(1, num_options))


def get_better_option(opt1: str, opt2: str, ind1: int, ind2: int) -> int:
    """Determines the better option, given two.

    Arguments:
        opt1 {str} -- The first option.
        opt2  {str} -- The second option.
        ind1 {int} -- The first option's index.
        ind2 {int} -- The second option's index.

    Returns:
        int -- The index of the bettwe option.
    """
    print(f'{ind1 + 1:2} -- {opt1}')
    print(f'{ind2 + 1:2} -- {opt2}')
    choice: int = int(
        input(f'Which is better {ind1 + 1} or {ind2 + 1}:\n')) - 1
    return choice


def rank_main(options: List[str]) -> List[int]:
    """Ranks the initial collection of options.

    Arguments:
        options {List[str]} -- The options to rank.

    Returns:
        List[int] -- The scores associated with each option.
    """
    # The points associated with each option.
    scores: List[int] = [0] * len(options)

    for i, opt1 in enumerate(options):
        for j, opt2 in enumerate(options):
            # If the options are not the same and haven't already been compared.
            if i != j and j > i:
                choice: int = get_better_option(opt1, opt2, i, j)
                scores[choice] += 1
    return scores


def rank_ties(options: List[str], scores: List[int]) -> List[int]:
    """Ranks the ties within the options.

    Arguments:
        options {List[str]} -- The options to rank.
        scores {List[int]} -- The scores associated with each option.

    Returns:
        List[int] -- The new scores with no ties.
    """
    # While there are duplicate scores in the list.
    while list(set(scores)) != sorted(scores):
        for i, score1 in enumerate(scores):
            for j, score2 in enumerate(scores):
                # If the options are not the same and have the same score.
                if i != j and score1 == score2:
                    choice: int = get_better_option(options[i], options[j], i,
                                                    j)
                    scores[choice] += 1
    return scores


def sort_scores(options: List[str], scores: List[int]) -> List[int]:
    """Sorts the options into the final comparison.

    Arguments:
        options {List[str]} -- The options to rank.
        scores {List[int]} -- The scores associated with each option.

    Returns:
        List[int] -- The ranked items in order.
    """
    # Zip the scores and the options together.
    zipped_pairs: zip = zip(scores, options)
    # Sort the zip.
    sort = reversed([e for _, e in sorted(zipped_pairs)])
    return sort


def main() -> None:
    """The main of the program.
    """
    # The options to rank.
    user_options: List[str] = []
    while True:
        tmp: str = input('Option:\n')
        if tmp == '':
            break
        user_options.append(tmp)
    print()

    # The points associated with each option.
    user_scores: List[int] = rank_main(user_options)
    print()
    user_scores = rank_ties(user_options, user_scores)
    print()

    # Sort the zip.
    sort = sort_scores(user_options, user_scores)
    num_len: int = len(str(len(user_scores)))
    score_len: int = max(len(str(e)) for e in user_scores)

    for i, opt in enumerate(sort):
        print(
            f'{i + 1:{num_len}} -- {user_scores[user_options.index(opt)]:{score_len}} -- {opt}'
        )


if __name__ == "__main__":
    print('Hello, Console!')
    print()

    main()
