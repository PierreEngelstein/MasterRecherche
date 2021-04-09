from math import sqrt
import cvxpy as cp
import numpy as np
from math import log2

def norm(fct):
    return sqrt(np.dot(np.transpose(fct), fct))

# Initial qubits states
''' Implementation of primal version optimal quantum detectors via SdP (https://arxiv.org/pdf/quant-ph/0205178.pdf) '''

phi_1, p1 = [[1], [0]], 0.1
phi_2, p2 = [[1/sqrt(2)], [1/sqrt(2)]], 0.6
phi_3, p3 = [[0], [1]], 0.3
# phi_3, p3 = [[1/3], [(2*sqrt(2))/3]], 0.3

# Compute p_i' = p_i * phi_i
rho_1prime = p1 * np.dot(phi_1, np.transpose(phi_1))
rho_2prime = p2 * np.dot(phi_2, np.transpose(phi_2))
rho_3prime = p3 * np.dot(phi_3, np.transpose(phi_3))
identity = np.identity(2)

Pi_1 = cp.Variable((2, 2))
Pi_2 = cp.Variable((2, 2))
Pi_3 = cp.Variable((2, 2))
constraints =  [Pi_1 >> 0]
constraints += [Pi_2 >> 0]
constraints += [Pi_3 >> 0]
constraints += [Pi_1 + Pi_2 + Pi_3 == identity]

obj = cp.Maximize(cp.trace(Pi_1 @ rho_1prime) + cp.trace(Pi_2 @ rho_2prime) + cp.trace(Pi_3 @ rho_3prime))

prob = cp.Problem(obj, constraints)
prob.solve()
Pi_1_sol = Pi_1.value
print(np.around(Pi_1_sol, 3))
print()
Pi_2_sol = Pi_2.value
print(np.around(Pi_2_sol, 3))
print()
Pi_3_sol = Pi_3.value
print(np.around(Pi_3_sol, 3))
print()
proba_correct = p1 * np.trace(np.dot(Pi_1_sol, np.dot(phi_1, np.transpose(phi_1)))) + p2 * np.trace(np.dot(Pi_2_sol, np.dot(phi_2, np.transpose(phi_2)))) + p3 * np.trace(np.dot(Pi_3_sol, np.dot(phi_3, np.transpose(phi_3))))
print(str(1-proba_correct))
print("**********")

def entropy_von_neumann(state):
    """
        Computes the Von Neumann entropy of a given density matrix.
        Parameters
        ----------
            state : Density matrix
    """
    eigenvals = np.linalg.eigvals(state)
    h = 0
    for i in eigenvals:
        if i > 0:
            h -= i * log2(i)
    return h

Phi_test_1 = np.dot(phi_2, np.transpose(phi_2)) * p2
print(Phi_test_1)
# Using kron for tensor product, not sure if simple matrix multiplication or kron product here ?
I_1 = entropy_von_neumann(Phi_test_1) + entropy_von_neumann(Pi_1_sol) - entropy_von_neumann(np.kron(Phi_test_1, Pi_1_sol))
print("I(Phi_1, Pi_1) = " + str(I_1))
print(np.dot(Phi_test_1, Pi_1_sol))
print()
print(np.kron(Phi_test_1, Pi_1_sol))

# print("H(Phi_test_1) = " + str(np.around(entropy(Phi_test_1), 3)))
# Phi_test_2 = [[0.5, 0], [0, 0.5]]
# print("H(Phi_test_2) = " + str(np.around(entropy(Phi_test_2), 3)))
# Phi_test_3 = np.dot(phi_1, np.transpose(phi_1))
# print("H(Phi_test_2) = " + str(np.around(entropy(Phi_test_3), 3)))
print()
a = [[-0.524],[0.849]]
print(np.dot(a, np.transpose(a)))
print(entropy_von_neumann(Phi_test_1))
print(entropy_von_neumann(np.dot(a, np.transpose(a))))
print(entropy_von_neumann(np.kron(Phi_test_1, np.dot(a, np.transpose(a)))))
print(entropy_von_neumann(Phi_test_1) + entropy_von_neumann(np.dot(a, np.transpose(a))) - entropy_von_neumann(np.kron(Phi_test_1, np.dot(a, np.transpose(a)))))

print("**********")

def entropy_shannon(matrix):
    H = 0
    for i in matrix:
        for j in i:
            H -= j * log2(j)
    return H

a = [[0.5], [0.1], [0.2], [0.2]]
b = [[0.1], [0.4], [0.2], [0.3]]
a_b = np.dot(a, np.transpose(b))
I_a_b = entropy_shannon(a) + entropy_shannon(b) - entropy_shannon(a_b)
print(np.around(I_a_b, 4))


print("**********")


def I(Mu_Vect, Phi_Vect):
    '''
       Computes mutual information from 2 sets of density operators.
    '''
    tr_mtx = np.zeros((len(Mu_Vect), len(Phi_Vect)))

    H_mu = 0
    H_Mu_Phi = 0
    for i in range(0, len(Mu_Vect)):
        sum_row = 0
        for j in range(0, len(Phi_Vect)):
            val = np.trace(np.dot(Mu_Vect[i], Phi_Vect[j]))
            if val < 1e-04: val = 0
            if val > 0: # Only positive values for log
                H_Mu_Phi -= val * log2(val)
            tr_mtx[i][j] = val
            sum_row += val
        if sum_row != 0:  # Only positive values for log
            H_mu -= sum_row * log2(sum_row)

    # H_Phi
    H_Phi = 0
    tr_mtx_t = np.transpose(tr_mtx)
    for i in range(0, len(tr_mtx_t)):
        sum_column = 0
        for j in range(0, len(tr_mtx_t[i])):
            sum_column += tr_mtx_t[i][j]
        if sum_column != 0:  # Only positive values for log
            H_Phi -= sum_column * log2(sum_column)

    return H_mu + H_Phi - H_Mu_Phi

mu_Vect = [Pi_1_sol, Pi_2_sol, Pi_3_sol]
# A good one 
mu_Vect = [[[0.6255946156, 0.375000003751], [0.444509082871, 0.26748142285]]  ,  [[0, 0], [0.021823459898, 0.265445434171]] , [[0.374405389634, -0.37499999475], [-0.466332533768, 0.46707313398]] ]
# A symetric one
# mu_Vect = [[[0.823093293514, 0.335635486626], [0.335635477626, 0.178134012135]]  ,  [[0.123383189926, -0.243314709776], [-0.243314700776, 0.662625197298]] , [[0.0535235075613, -0.0923207678493], [-0.0923207678493, 0.159240781568]] ]
phi_Vect= [rho_1prime, rho_2prime, rho_3prime]

I_mu_phi = I(mu_Vect, phi_Vect)
print("I(Mu, Phi) = " + str(np.around(I_mu_phi, 3)))
