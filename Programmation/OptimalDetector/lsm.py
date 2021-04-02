''' Implementation of optimal quantum detectors via least square measurement (https://arxiv.org/pdf/quant-ph/0005132.pdf) '''
from math import sqrt
import cvxpy as cp
import numpy as np
import scipy
from matplotlib import pyplot as plt

def Minimize_LSM(args: tuple, weights: tuple = None, debug: bool = False, useSVD: bool = False):
    phi = np.hstack(args)
    if weights is not None: # Multiply phi by W if weighted
        if len(args) != len(weights):
            print("Inconsistent lengths (args: " + str(len(args)) + ", weights: " + str(len(weights)) + ")")
            return 0, 0
        if sum(weights) - 1.0 > 1e-05:
            print("Inconsistent weights: sum " + str(sum(weights)) + " not equal to 1")
            return 0, 0
        W = np.identity(len(weights))

        for i in range(0, len(weights)):
            W[i][i] = weights[i]
        if debug:
            print("W = ")
            print(W)

        phi = np.dot(phi, W)

    if len(args) > len(args[0]) :
        print("Incorrect data, too much state vectors.")
        return 0, 0
    if debug:
        print("phi = ")
        print(phi)
    
    if useSVD: # Using Single Value Decomposition (a bit faster)
        if debug: print("Using SVD for optimum matrix")
        u , s, v = np.linalg.svd(phi)
        M_opti = np.dot(u, np.transpose(np.matrix(v).getH()))
    else:
        if debug: print("Not using SVD for optimum matrix")
        _ , s, _ = np.linalg.svd(phi)
        # Using np.real to remove approx. errors which lead to complex numbers with imaginary part almost 0j
        M_opti = np.real(np.dot(phi, np.linalg.pinv(scipy.linalg.sqrtm(np.dot(np.matrix(phi).getH(), phi)))))

    if debug:
        print(M_opti)

    if debug:
        for i in range(0, len(args)):
            print("mu_" + str(i+1) + " = " + str(M_opti[:,i]))

    if weights is not None: # Weighted error, multiply result by W
        error = np.trace(np.dot(np.dot(np.matrix(phi - M_opti).getH(), (phi - M_opti)), W))
    else: # Non weighted error
        error = np.trace(np.dot(np.matrix(phi - M_opti).getH(), (phi - M_opti)))

    err_min = 0
    for i in range(0, len(s)):
        err_min += (1 + s[i])**2
    return err_min, error

# Experiment 1: non weighted detection (equal probability for each state)

print("EXP 1: non weighted detection")
# n=1
phi_1 = [[1/3], [(2*sqrt(2)/3)]]
phi_2 = [[-1/2], [sqrt(3)/2]]
# n=2
phi_3 = [[1/2], [1/2], [1/2], [1/2]]
phi_4 = [[1/3], [0], [(2*sqrt(2)/3)], [0]]
phi_5 = [[0], [1/4], [0], [(sqrt(15)/4)]]
err_min, error = Minimize_LSM((phi_1, phi_2), debug=True, useSVD=True)
print("error = " + str(np.around(error*100, 3)) + "%")
print("*****")
err_min, error = Minimize_LSM((phi_1, phi_2), debug=True, useSVD=False)
print("error = " + str(np.around(error*100, 3)) + "%")

print("\n**********\n**********\n")

# Experiment 2: weighted detection (non equal probability for each vector)
print("EXP 2: weighted detection")
err_min, error = Minimize_LSM((phi_1, phi_2), weights=(0.45, 0.55), useSVD=True)
print("error = " + str(np.around(error*100, 3)) + "%")
# Test with n=2 qubits (H dim 4 instead of 2)
err_min, error = Minimize_LSM((phi_3, phi_4, phi_5, phi_4), weights=(0.45, 0.45, 0.05, 0.05), useSVD=False, debug=True)
print("error = " + str(np.around(error*100, 3)) + "%")


x = np.arange(0, 1, 0.01)
y = []
for i in x:
    err_min, error = Minimize_LSM((phi_1, phi_2), weights=(i, 1-i), useSVD=True)
    y.append(error)

plt.plot(x, y)
plt.show()