from math import sqrt
import cvxpy as cp
import numpy as np
from math import log2, log

def norm(fct):
    return sqrt(np.dot(np.transpose(fct), fct))

# Initial qubits states
''' Implementation of primal version optimal quantum detectors via SdP (https://arxiv.org/pdf/quant-ph/0205178.pdf) '''

phi_1, p1 = [[1], [0]], 0.1
phi_2, p2 = [[1/sqrt(2)], [1/sqrt(2)]], 0.6
phi_3, p3 = [[0], [1]], 0.3
# phi_3, p3 = [[1/3], [(2*sqrt(2))/3]], 0.3

phi_1, p1 = [[1], [0]], 0.1
phi_2, p2 = [[0], [1]], 0.9
phi_3, p3 = [[0], [1]], 0

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

def matrix_from_ibex(value: str):
    value = value.replace("(", "")
    value = value.replace(")", "")
    value = value.split(" ; ")
    matrix_1 = [[float(value[0]), float(value[1])], [float(value[1]), float(value[2])]]
    matrix_2 = [[float(value[3]), float(value[4])], [float(value[4]), float(value[5])]]
    matrix_3 = [[float(value[6]), float(value[7])], [float(value[7]), float(value[8])]]
    return matrix_1, matrix_2, matrix_3

mu_Vect = [Pi_1_sol, Pi_2_sol, Pi_3_sol]
# A good one 
mu_Vect = [[[0.6255946156, 0.375000003751], [0.444509082871, 0.26748142285]]  ,  [[0, 0], [0.021823459898, 0.265445434171]] , [[0.374405389634, -0.37499999475], [-0.466332533768, 0.46707313398]] ]
# A symetric one
# mu_Vect = [[[0.823093293514, 0.335635486626], [0.335635477626, 0.178134012135]]  ,  [[0.123383189926, -0.243314709776], [-0.243314700776, 0.662625197298]] , [[0.0535235075613, -0.0923207678493], [-0.0923207678493, 0.159240781568]] ]
# Another symetric one
# mu_Vect = [[[0.494309400282, 0.46042366814], [0.46042366814, 0.525919152913]]  ,  [[0.215181242609, -0.227882790059], [-0.227882790059, 0.287941374384]] , [[0.29050934811, -0.232540869079], [-0.232540869079, 0.186139481704]] ]

phi_Vect= [rho_1prime, rho_2prime, rho_3prime]

I_mu_phi = I(mu_Vect, phi_Vect)
print("I(Mu, Phi) = " + str(np.around(I_mu_phi, 3)))

m1, m2, m3 = matrix_from_ibex("(1.39583601254e-09 ; 5.55111512313e-17 ; 0.71641653534 ; 0.68422745826 ; 0.247453318469 ; 0.089547880248 ; 0.315772549345 ; -0.247453309468 ; 0.194035593413)")
m1, m2, m3 = matrix_from_ibex("(0.68749999125 ; 0.0719868354806 ; 0.5 ; 0.187500003751 ; -0.075894663844 ; 0.499877827058 ; 0.124999996001 ; 0.00390783736354 ; 0.000122181942225)")

def I1(m, p):
    h_m = 0
    for i in range(0, len(m)):
        sum = 0
        for j in range(0, len(p)):
            sum += np.trace(np.dot(p[j], m[i]))
        if sum > 1e-06:
            h_m += sum * log2(sum)
    h_p = 0
    for i in range(0, len(p)):
        sum = 0
        for j in range(0, len(m)):
            sum += np.trace(np.dot(p[i], m[j]))
        if sum > 1e-06:
            h_p += sum * log2(sum)

    h_m_p = 0
    for i in range(0, len(p)):
        for j in range(0, len(m)):
            if np.trace(np.dot(p[i], m[j])) > 1e-06:
                h_m_p += np.trace(np.dot(p[i], m[j])) * log2(np.trace(np.dot(p[i], m[j])))
    return -(h_m + h_p - h_m_p)

i = I1([m1, m2, m3], phi_Vect)
print(i)

# i = I1([(1/3) * np.identity(2), (1/3) * np.identity(2), (1/3) * np.identity(2)], phi_Vect)
# print(i)

i = I1([Pi_1_sol, Pi_2_sol, Pi_3_sol], phi_Vect)
print(i)

i = I1([[[0, 0], [0, 1]], [[1, 0], [0, 0]]], [[[0.45, 0], [0, 0]], [[0, 0], [0, 0.55]]])
# print(i)

print(-0.1*log2(0.1) - 0.9*log2(0.9))
x = np.arange(0.1, 1, 0.0001)
y = []
for i in x:
    y.append(i * log(i))

from matplotlib import pyplot as plt
plt.plot(x, y)
plt.grid()
plt.show()


