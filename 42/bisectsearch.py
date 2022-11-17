# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 bisectsearch.py
# ------------------------------------------------------------------------------
"""The bisectsearch module provides functions to search sorted keys.

It requires that the search key type implements the < {__lt__} method.

Although binarysearch.py meets the theoretical lower bound for minimum
number of compares, bisectsearch.py is likely faster because the underlying
implementation is written in C instead of Python.

@citation Adapted from: https://docs.python.org/3/library/bisect.html
Accessed 2021/06/06.

@author Kaya Unalmis
"""

import bisect


def first(key, keys, lo: int = 0, hi: int = -1) -> int or None:
    """
    :param key:  search key
    :param keys: sorted keys
    :param lo:   lower bound in search range, defaults to 0
    :param hi:   upper bound in search range, defaults to len(keys)
    :return:     first index of key in keys[lo:hi); None if there is no such key
    """
    if hi == -1:
        hi = len(keys)
    i = bisect.bisect_left(keys, key, lo, hi)
    return i if (i < hi and (not key < keys[i])) else None


def last(key, keys, lo: int = 0, hi: int = -1) -> int or None:
    """
    :param key:  search key
    :param keys: sorted keys
    :param lo:   lower bound in search range, defaults to 0
    :param hi:   upper bound in search range, defaults to len(keys)
    :return:     last index of key in keys[lo:hi); None if there is no such key
    """
    if hi == -1:
        hi = len(keys)
    i = bisect.bisect_right(keys, key, lo, hi)
    return i - 1 if (i < hi + 1 and (not keys[i - 1] < key)) else None


def floor(key, keys, lo: int = 0, hi: int = -1) -> int or None:
    """
    :param key:  search key
    :param keys: sorted keys
    :param lo:   lower bound in search range, defaults to 0
    :param hi:   upper bound in search range, defaults to len(keys)
    :return:     index of largest key in keys[lo:hi) less than or equal to key;
                 None if there is no such key
    """
    if hi == -1:
        hi = len(keys)
    i = bisect.bisect_right(keys, key, lo, hi)
    return i - 1 if i > lo else None


def ceiling(key, keys, lo: int = 0, hi: int = -1) -> int or None:
    """
    :param key:  search key
    :param keys: sorted keys
    :param lo:   lower bound in search range, defaults to 0
    :param hi:   upper bound in search range, defaults to len(keys)
    :return:     index of smallest key in keys[lo:hi) greater than or equal to key;
                 None if there is no such key
    """
    if hi == -1:
        hi = len(keys)
    i = bisect.bisect_left(keys, key, lo, hi)
    return i if i < hi else None


def main():
    """Unit tests the bisectsearch module."""

    #        0    1    2    3    4    5    6    7
    keys = ("B", "B", "C", "G", "G", "T", "T", "T")

    assert first("Z", keys) is None
    assert last("Z", keys) is None
    assert first("G", keys) == 3
    assert last("G", keys) == 4

    assert floor("A", keys) is None
    assert floor("Z", keys) == len(keys) - 1
    assert ceiling("Z", keys) is None
    assert ceiling("A", keys) == 0

    assert 3 <= floor("G", keys) <= 4
    assert 3 <= ceiling("G", keys) <= 4


if __name__ == "__main__":
    main()
