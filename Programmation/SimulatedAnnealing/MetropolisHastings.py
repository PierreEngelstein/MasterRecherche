'''
Implementation of the Metropolis-Hastings algorithm for invert exponential distribution.
'''

from math import exp, sin, cos
import numpy as np
import matplotlib.pyplot as plt

def target(x):
    if x < 0:
        return 0
    return exp(-x)

amount = 10000

x = [0] * amount
x[1] = 3

for i in range(2, amount):
    current_x = x[i-1]
    proposed_x = current_x + np.random.normal(loc=0, scale=1, size=None)
    A = target(proposed_x)/target(current_x)
    runif = np.random.uniform(low=0, high=1, size=None)
    if(runif < A):
        x[i] = proposed_x
    else:
        x[i] = current_x

plt.subplot(121)
plt.plot(range(0, amount), x)
plt.subplot(122)
n, bins, patches = plt.hist(x=x)
plt.grid(axis='y')
plt.xlabel('Value')
plt.ylabel('Frequency')
maxfreq = n.max()
plt.show()