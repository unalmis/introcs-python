# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 eulertotient_function.py 1 11
# phi(  1) =   1
# phi(  2) =   1
# phi(  3) =   2
# phi(  4) =   2
# phi(  5) =   4
# phi(  6) =   2
# phi(  7) =   6
# phi(  8) =   4
# phi(  9) =   6
# phi( 10) =   4
# ...
# phi(495) = 240
# phi(496) = 240
# phi(497) = 420
# phi(498) = 164
# phi(499) = 498
# phi(500) = 200
# ------------------------------------------------------------------------------
"""Euler’s totient is an important function in number theory.

Psi(n) is defined as the number of positive integers less than or equal to n
that are relatively prime with n (no factors in common with n other than 1).
This program computes Psi(n) by implementing an analytic formula.

@author Kaya Unalmis
"""

import sys


def euler_totient(n: int) -> int:
    # return number of positive ints <= n that are relatively prime with n

    # phi(n) = n pi_prod (1 - 1/p) for all prime factors p of n
    phi = n
    f = 2
    # @citation Adapted from:
    # Introduction to Programming in Python.
    # Addison-Wesley Professional, 2015, pp. 81,
    # by Robert Sedgewick, Kevin Wayne, Robert Dondero.
    while f * f <= n:
        if n % f == 0:
            phi *= 1 - 1 / f
            n //= f
            # cast out factor
            while n % f == 0:
                n //= f
        f += 1

    if n > 1:
        phi *= 1 - 1 / n
    return round(phi)


# write the euler totient function on interval [lo, hi)
lo = max(1, int(sys.argv[1]))
hi = max(1, int(sys.argv[2]))
for i in range(lo, hi):
    print(f"phi({i}) = {euler_totient(i)}")
