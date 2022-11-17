# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 staticdiscrete.py 20
# ------------------------------------------------------------------------------

from random import uniform
from typing import Tuple

from bisectsearch import ceiling


class StaticDiscrete:
    """Fast, O(lg N), random number generation from discrete distributions

    Construction takes linear time and space in the worst case.

    @author Kaya Unalmis
    """

    _s: Tuple[int or float, ...]

    def __init__(self, p):
        """Make immutable random number generator.

        :param p: the discrete distribution to sample from
        """
        s = list(p)
        for i in range(1, len(s)):
            s[i] += s[i - 1]  # form cumulative sums
        self._s = tuple(s)

    def random(self) -> int:
        """:return: the index i with probability p[i]"""
        # _s[-1] = last index of _s[] = the sum of _s[]
        return ceiling(uniform(0, self._s[-1]), self._s)


def main():
    """Unit tests the StaticDiscrete data type."""
    import sys

    n = int(sys.argv[1])
    discrete = StaticDiscrete([1 / n] * n)  # uniform
    for i in range(n):
        print(discrete.random())


if __name__ == "__main__":
    main()
