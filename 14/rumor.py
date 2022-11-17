# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 rumor.py 7 10000
# A rumor spreads at a 7 guest party.
# After 10000 trials, the
# probability (%) all guests hear it is 3.75
# expected number of guests to hear it is 4.5232
# ------------------------------------------------------------------------------
"""Rumor propagation.

This program estimates the probability that everyone at the party (except Alice)
hears the rumor before it stops propagating, and the expected number of people
that will hear the rumor.

Alice is throwing a party with n other guests, including Bob.
Bob starts a rumor about Alice by telling it to one of the other guests.
A person hearing this rumor for the first time will immediately tell it to one
other guest, chosen at random from all the people at the party except Alice and
the person from whom they heard it. If a person (including Bob) hears the rumor
for a second time, he or she will not propagate it further.
"""

import random
import sys

# simulate rumor propagation at a party with n guests for t trials
n = max(1, int(sys.argv[1]))
trials = max(1, int(sys.argv[2]))

heardByAll = 0
heardCountSum = 0

for t in range(trials):
    heard = [False] * n
    heardCount = 0

    src = None
    cur = 0
    # rumor stops propagating when the current person has already heard
    while not heard[cur]:
        heard[cur] = True
        heardCount += 1
        if heardCount >= n:
            break
        # select next guest to hear rumor
        r = random.randrange(0, n)
        while r == src or r == cur:
            r = random.randrange(0, n)
        src = cur
        cur = r

    # update stats
    heardCountSum += heardCount
    if heardCount >= n:
        heardByAll += 1

print("A rumor spreads at a " + str(n) + " guest party.")
print("After " + str(trials) + " trials, the")
print("probability (%) all guests hear it is", 100 * heardByAll / trials)
print("expected number of guests to hear it is", heardCountSum / trials)
