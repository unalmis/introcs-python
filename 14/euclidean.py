# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 euclidean.py 12 25
# vector a: [3, 17, 3, 17, 17, 18, 7, 20, 0, 14, 17, 17]
# vector b: [22, 1, 22, 8, 3, 2, 21, 24, 10, 20, 20, 1]
# euclidean distance between a and b: 46.08687448721165
# ------------------------------------------------------------------------------

import math
import random
import sys

# compute euclidean distance between two vectors of length n bounded by m
n = int(sys.argv[1])
m = int(sys.argv[2])

# make arrays of length n filled with random ints [0, m)
a = [0] * n
b = [0] * n
for i in range(n):
    a[i] = random.randrange(0, m)
    b[i] = random.randrange(0, m)

dist = 0
for i in range(n):
    delta = a[i] - b[i]
    dist += delta * delta
dist = math.sqrt(dist)

print("vector a:", a)
print("vector b:", b)
print("euclidean distance between a and b:", dist)
