'''
Implementation of the simulated annealing algorithm.
'''

import numpy as np
import matplotlib.pyplot as plt
from random import uniform
from math import exp, cos, sin

interval = (-50, 100)

# Function to optimize
def f(x):
    return (x**2)*sin(x**3 * cos(x**2))

def clip(x):
    a, b = interval
    return max(min(x, b), a)

def random_start():
    a, b = interval
    return uniform(a, b)

def cost_function(x):
    return f(x)

# Find a random point around x
def random_neighbour(x, fraction=1):
    amplitude = (max(interval) - min(interval)) * fraction / 10
    delta = (-amplitude/2) + amplitude * np.random.random_sample()
    return clip(x + delta)

def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        return 1
    else:
        return np.exp(- (new_cost - cost) / temperature)

# Defines the criteria of acceptance of the new state / cost
def MetropolisCriteria(delta, temperature):
    if delta < 0:
        return True
    if(np.random.random() < exp(-delta / temperature)):
        return True
    return False

# Compute temperature of the system (cooling linearly or by step)
def temperature(fraction):
    return max(0.01, min(1, 1 - fraction))

# Annealing process
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

        if(MetropolisCriteria(new_cost - cost, T)):
            state, cost = new_state, new_cost
            states.append(state)
            costs.append(cost)
    
    return state, cost_function(state), states, costs

state, cost, states, costs = annealing(maxsteps=1000)

print(state, cost)


plt.figure()
plt.subplot(131)
plt.plot(states)
plt.subplot(132)
plt.plot(costs)
plt.subplot(133)
# Plot the minimal value found
xs = np.arange(min(interval), max(interval), 0.01)
ys = (list(map(f, xs)))
plt.plot(xs, ys)
plt.axvline(x=state, color='r')
plt.show()