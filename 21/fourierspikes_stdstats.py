# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 fourierspikes_stdstats.py 50 500
# ------------------------------------------------------------------------------
"""Plots the fourier spike.

Takes two command-line arguments, n and m, and plots the function
(cos(t) + cos(2 t) + cos(3 t) +. . . + cos(N t)) / N
for m equally spaced samples of t across the origin.
The sum converges to a spike (0 everywhere except a single value).
This property is the basis for a proof that any smooth function can be
expressed as a sum of sinusoids.

@author Kaya Unalmis
"""

import math
import sys

import stddraw
import stdstats


def cos_sum(n: int, t: float) -> float:
    # return (1/n) sigma, from i = 1 to n, of cos(i * t)
    value = 0
    for i in range(1, n + 1):
        value += math.cos(i * t)
    return value / n


def function_samples(f, n: int, samples: int, start: float, stop: float) -> list:
    # return f(n, t) for {samples} samples from t = start to t = stop
    step_size = (stop - start) / samples
    y = [0.0] * (samples + 1)
    for i in range(len(y)):
        t = start + i * step_size
        y[i] = f(n, t)
    return y


def plot(
    f,
    n: int,
    samples: int = 500,
    start: float = -math.pi / 2,
    stop: float = math.pi / 2,
):
    # plot the f function taking {samples} samples
    y = function_samples(f, n, samples, start, stop)
    stddraw.setYscale(min(y), max(y))
    stdstats.plotLines(y)


# Here we are passing a function object as parameter. For more info see
# Introduction to Programming in Python.
# Addison-Wesley Professional, 2015, pp. 478,
# by Robert Sedgewick, Kevin Wayne, Robert Dondero.
plot(cos_sum, int(sys.argv[1]), int(sys.argv[2]))  # n, samples
stddraw.show()
