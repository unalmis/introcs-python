# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 convertbase.py 256 8
# ------------------------------------------------------------------------------
"""Convert a given decimal number to the specified base representation.

@author Kaya Unalmis
"""


def convert_base10(d: int, base: int) -> list:
    """
    :param d:    an integer >= 0 to convert from base 10 to the specified base
    :param base: the base to convert to
    :return:     string representation of d in given base
    """
    a = list()
    if d == 0:
        a.append(0)

    while d > 0:
        a.append(d % base)
        d //= base
    a.reverse()
    return a


def main():
    """Unit tests the convertbase module."""
    import sys

    d = int(sys.argv[1])
    base = int(sys.argv[2])
    print(convert_base10(d, base))


if __name__ == "__main__":
    main()
