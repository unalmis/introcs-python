# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 ramanujan.py 30000
# 1729 = 1^3 + 12^3 = 9^3 + 10^3
# 4104 = 2^3 + 16^3 = 9^3 + 15^3
# 13832 = 2^3 + 24^3 = 18^3 + 20^3
# 20683 = 10^3 + 27^3 = 19^3 + 24^3
# ------------------------------------------------------------------------------
"""Ramanujan's taxi.

Finds all integers up to n expressible as a sum of 2 positive cubes in 2 ways.
Finds distinct positive integers a, b, c, and d such that a^3 + b^3 = c^3 + d^3.
"""

import sys

# maximum number to search up to
n = int(sys.argv[1])

# for each a, b, c, d, check whether a^3 + b^3 = c^3 + d^3
# start values chosen to avoid duplicates
for a in range(1, n + 1):
    a3 = a * a * a
    if a3 > n:
        break

    for b in range(a, n + 1):
        b3 = b * b * b
        a3b3 = a3 + b3
        if a3b3 > n:
            break

        for c in range(a + 1, n + 1):
            c3 = c * c * c
            if c3 > a3b3:
                break

            for d in range(c, n + 1):
                d3 = d * d * d
                c3d3 = c3 + d3
                if c3d3 > a3b3:
                    break

                if c3d3 == a3b3:
                    print(f"{a3b3} = {a}^3 + {b}^3 + {c}^3 + {d}^3")
