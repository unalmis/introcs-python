# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 fourierspikes.py 50 500
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


def cos_sum(n: int, t: float) -> float:
    # return (1/n) sigma, from i = 1 to n, of cos(i * t)
    value = 0
    for i in range(1, n + 1):
        value += math.cos(i * t)
    return value / n


def cos_sum_x(samples: int, start: float, stop: float) -> list:
    # return cos_sum input for {samples} samples from t = start to t = stop
    step_size = (stop - start) / samples
    x = [0.0] * (samples + 1)
    for i in range(len(x)):
        x[i] = start + i * step_size
    return x


def cos_sum_y(n: int, x: list) -> list:
    # return cos_sum(n, t) output given input x[]
    y = [0.0] * len(x)
    for i in range(len(y)):
        y[i] = cos_sum(n, x[i])
    return y


def plot(
    n: int, samples: int = 500, start: float = -math.pi / 2, stop: float = math.pi / 2
):
    # plot the cos_sum(n..) function taking {samples} samples

    x = cos_sum_x(samples, start, stop)
    y = cos_sum_y(n, x)

    stddraw.setXscale(start, stop)
    stddraw.setYscale(min(y), max(y))
    stddraw.setPenRadius(0.0)
    for i in range(samples):
        stddraw.line(x[i], y[i], x[i + 1], y[i + 1])


plot(int(sys.argv[1]), int(sys.argv[2]))  # n, samples
stddraw.show()
