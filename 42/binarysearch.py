# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 binarysearch.py
# ------------------------------------------------------------------------------
"""The binarysearch module provides functions to search sorted keys.

It requires that the search key type implements the < {__lt__} method.

Each function makes 1 + ⌈lg N⌉ compares in the worst case, where N is the
number of keys in the search range. This implementation uses iteration instead
of recursion due to overhead associated with recursion in Python.

@author Kaya Unalmis
"""


def index(key, keys, lo: int = 0, hi: int = -1) -> int or None:
    """
    :param key:  search key
    :param keys: sorted keys
    :param lo:   lower bound in search range, defaults to 0
    :param hi:   upper bound in search range, defaults to len(keys)
    :return:     index of key in keys[lo:hi); None if there is no such key
    """
    # @citation Adapted from: Robert Sedgewick and Kevin Wayne.
    # Algorithms, 4th edition. Addison-Wesley Professional, 2011, pp. 9.

    if hi == -1:
        hi = len(keys)
    hi -= 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if key < keys[mid]:
            hi = mid - 1
        elif keys[mid] < key:
            lo = mid + 1
        else:
            return mid
    return None


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
    hi -= 1

    champ = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if key < keys[mid]:
            hi = mid - 1
        elif keys[mid] < key:
            lo = mid + 1
        else:  # store the match, restart search on lower half
            champ = mid
            hi = mid - 1
    return champ


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
    hi -= 1

    champ = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if key < keys[mid]:
            hi = mid - 1
        elif keys[mid] < key:
            lo = mid + 1
        else:  # store the match, restart search on upper half
            champ = mid
            lo = mid + 1
    return champ


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
    hi -= 1

    champ = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if key < keys[mid]:
            hi = mid - 1
        elif keys[mid] < key:
            champ = mid
            lo = mid + 1
        else:
            return mid
    return champ


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
    hi -= 1

    champ = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if key < keys[mid]:
            champ = mid
            hi = mid - 1
        elif keys[mid] < key:
            lo = mid + 1
        else:
            return mid
    return champ


def main():
    """Unit tests the binarysearch module."""

    #        0    1    2    3    4    5    6    7
    keys = ("B", "B", "C", "G", "G", "T", "T", "T")

    assert index("Z", keys) is None
    assert first("Z", keys) is None
    assert last("Z", keys) is None
    assert first("G", keys) == 3
    assert last("G", keys) == 4

    assert floor("A", keys) is None
    assert floor("Z", keys) == len(keys) - 1
    assert ceiling("Z", keys) is None
    assert ceiling("A", keys) == 0

    assert 5 <= index("T", keys) <= 7
    assert 3 <= floor("G", keys) <= 4
    assert 3 <= ceiling("G", keys) <= 4


if __name__ == "__main__":
    main()
