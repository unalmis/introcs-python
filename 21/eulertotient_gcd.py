# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 eulertotient_gcd.py 1 11
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
This program computes Psi(n) by using the greatest common divisor algorithm.

@author Kaya Unalmis
"""

import sys


def is_relatively_prime(x: int, y: int) -> bool:
    # do x and y share only the common factor 1?
    while y != 0:  # Euclid's algorithm
        temp = y
        y = x % y
        x = temp
    return x == 1  # greatest common divisor == 1


def euler_totient(n: int) -> int:
    # return number of positive ints <= n that are relatively prime with n
    phi = 1
    for x in range(2, n):
        # 1 and n are relatively prime, n and n not relatively prime
        if is_relatively_prime(x, n):
            phi += 1
    return phi


# write the euler totient function on interval [lo, hi)
lo = max(1, int(sys.argv[1]))
hi = max(1, int(sys.argv[2]))
for i in range(lo, hi):
    print(f"phi({i}) = {euler_totient(i)}")
