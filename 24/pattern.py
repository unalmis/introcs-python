# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 pattern.py 6 glider
# python3 pattern.py 8 random 0.25
# ------------------------------------------------------------------------------
"""Helper module for life.py."""

import stddraw
from stdarray import create2D
from stdrandom import bernoulli


def random(n: int, p: float = 0.25) -> list:
    """
    :param n: boolean list size
    :param p: probability an entry in the list is true
    :return:  n by n list where an entry is True with probability p
    """
    a = create2D(n, n)
    for i in range(n):
        for j in range(n):
            a[i][j] = bernoulli(p)
    return a


def glider(n: int = 6) -> list:
    """
    :param n: boolean list size
    :return:  n by n list with a glider pattern
    :raise ValueError: if n is less than 6
    """
    if n < 6:
        raise ValueError
    a = create2D(n, n, False)
    mid = n // 2 - 1
    a[mid][mid] = True
    a[mid][mid - 1] = True
    a[mid][mid + 1] = True
    a[mid - 1][mid + 1] = True
    a[mid - 2][mid] = True
    return a


def draw(pattern):
    """Draws pattern to stddraw. Client responsible for calling show().

    :param pattern: n by n boolean pattern
    """
    n = len(pattern)
    stddraw.setXscale(-1, n)
    stddraw.setYscale(-1, n)
    for i in range(n):
        for j in range(n):
            if pattern[i][j]:
                stddraw.setPenColor(stddraw.BOOK_LIGHT_BLUE)
                stddraw.filledSquare(j, n - 1 - i, 0.5)
            stddraw.setPenColor(stddraw.GRAY)
            stddraw.square(j, n - 1 - i, 0.5)


def main():
    """Pattern module test client.

    See example executions at bottom of file. Requires arguments:
        n, pattern size
        r, either 'glider' or 'random'
            if random selected a float between 0 and 1 required.

    :raise IndexError: if there is an insufficient number of arguments
    """
    import sys

    n = int(sys.argv[1])
    r = sys.argv[2]
    if r == "random":
        p = float(sys.argv[3])
        pattern = random(n, p)
    else:
        pattern = glider(n)
    draw(pattern)
    stddraw.show()


if __name__ == "__main__":
    main()
