'''
Implementation of the simulated annealing algorithm.
'''

import numpy as np
import matplotlib.pyplot as plt
from random import uniform
from math import exp, cos

interval = (-10, 10)

# Function to optimize
def f(x):
    return np.abs(x)

def clip(x):
    a, b = interval
    return max(min(x, b), a)

def random_start():
    a, b = interval
    return uniform(a, b)

def cost_function(x):
    return f(x)

def random_neighbour(x, fraction=1):
    amplitude = (max(interval) - min(interval)) * fraction / 10
    delta = (-amplitude/2) + amplitude * np.random.random_sample()
    return clip(x + delta)

def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        return 1
    else:
        return np.exp(- (new_cost - cost) / temperature)

def temperature(fraction):
    return max(0.01, min(1, 1 - fraction))

def annealing(maxsteps = 1000):
    state = random_start()
    print("initial state: " + str(state))
    cost = cost_function(state)
    states, costs = [state], [cost]
    for step in range(maxsteps):
        fraction = step / float(maxsteps)
        T = temperature(fraction)
        new_state = random_neighbour(state, fraction)
        new_cost = cost_function(new_state)
        if(acceptance_probability(cost, new_cost, T) > np.random.random()):
            state, cost = new_state, new_cost
            states.append(state)
            costs.append(cost)
    
    return state, cost_function(state), states, costs

state, cost, states, costs = annealing(maxsteps=1000)

print(state, cost)

plt.figure()
plt.subplot(121)
plt.plot(states)
plt.subplot(122)
plt.plot(costs)
plt.show()