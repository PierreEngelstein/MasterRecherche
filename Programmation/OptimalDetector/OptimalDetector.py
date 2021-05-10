''' Implementation of dual version optimal quantum detectors via SdP (https://arxiv.org/pdf/quant-ph/0205178.pdf) '''

from math import sqrt
import cvxpy as cp
import numpy as np
import time
from matplotlib import pyplot as plt

def optimal_matrices(rho_vect):
    size_len = len(rho_vect[0][0])
    X = cp.Variable((size_len, size_len), symmetric=True)
    constraints = []
    for i in rho_vect:
        constraints += [X >> i]
    pb = cp.Problem(cp.Minimize(cp.trace(X)), constraints)
    pb.solve()
    X_sol = X.value
    
    tp = ()
    qs = []
    for i in rho_vect:
        X_p = X_sol - i
        w, v = np.linalg.eig(X_p)
        q = np.transpose([v[:,list(w).index(min(w))]])
        qs.append(q)
        q_v = np.transpose([np.hstack((np.dot(q, np.transpose(q))[:,0], np.dot(q, np.transpose(q))[:,1]))])
        tp = tp + (q_v,)
    Y = np.hstack(tp)
    sz = np.dot(np.linalg.inv(np.dot(np.transpose(Y), Y)), np.transpose(Y)).shape[1]
    b = np.zeros((sz, 1))
    b[0] = 1
    b[sz - 1] = 1
    solution = np.dot( np.dot(np.linalg.inv(np.dot(np.transpose(Y), Y)), np.transpose(Y)) , b )

    mu_vect = []
    for i in range(0, len(qs)):
        a = round(solution[i][0], 8)
        mu = sqrt(abs(a)) * qs[i]
        mu_vect.append(mu)

    return mu_vect

def norm(fct):
    return sqrt(np.dot(np.transpose(fct), fct))

# Graph time for amount of input quantum states
result = []
for k in range(2, 1000):
    vect = []
    start = 1
    end = k
    print(k)
    proba = (1/(end - start))
    for i in range(start, end):
        psi = [[1/i], [(sqrt((i**2)-1))/i]]
        psi_inv = [[(sqrt((i**2)-1))/i], [1/i]]
        rho = proba * np.dot(psi, np.transpose(psi))
        rho_inv = proba * np.dot(psi_inv, np.transpose(psi_inv))
        vect.append(rho)
        vect.append(rho_inv)
    now = time.time()
    mu_vect = optimal_matrices(vect)
    delta = time.time() - now
    result.append(delta)

plt.plot(range(2, 1000), result)
plt.title("Temps d'optimisation en fonction du nombre de matrices de densité d'entrées")
plt.xlabel("Nombre de matrices de densité d'entrées")
plt.ylabel("Temps d'optimisation (secondes)")
plt.show()


# Initial qubits states
psi_1, p1 = [[0], [1]], 0.4
psi_2, p2 = [[1/sqrt(2)], [1/sqrt(2)]], 0.6
# Compute p_i' = p_i * psi_i
rho_1prime = p1 * np.dot(psi_1, np.transpose(psi_1))
rho_2prime = p2 * np.dot(psi_2, np.transpose(psi_2))
rho_3prime = p2 * np.dot(psi_2, np.transpose(psi_2))
now = time.time()
mu_vect = optimal_matrices([rho_1prime, rho_2prime])
delta = time.time() - now
print("solve time: " + str(delta) + " seconds")

for i in mu_vect:
    # print(np.dot(i, np.transpose(i)))
    pi = np.dot(i, np.transpose(i))
    # print(pi)
    # print("**********")
1/0
# Formulate the problem and constraints, and solve
X = cp.Variable((2, 2), symmetric=True)
constraints =  [X >> rho_1prime]
constraints += [X >> rho_2prime]
constraints += [X >> rho_3prime]
prob = cp.Problem(cp.Minimize(cp.trace(X)), constraints)
prob.solve()
X_sol = X.value
print("Probability of correct detection: " + "{0:0.1f}%".format(np.trace(X_sol)*100)) # Proba of correct detection is the trace of matrix
print("Solution:")
print(X_sol)

X_p1 = X_sol - rho_1prime
X_p2 = X_sol - rho_2prime
X_p3 = X_sol - rho_3prime

# X_sol - p1'
w, v = np.linalg.eig(X_p1)
q1 = np.transpose([v[:,list(w).index(min(w))]])
# X_sol - p2'
w, v = np.linalg.eig(X_p2)
q2 = np.transpose([v[:,list(w).index(min(w))]])
# X_sol - p3'
w, v = np.linalg.eig(X_p3)
q3 = np.transpose([v[:,list(w).index(min(w))]])
print()
print("q1: ")
print(q1)
print("q2: ")
print(q2)
print("q3: ")
print(q3)

# Matrix of equation 38
q1_v = np.transpose([np.hstack((np.dot(q1, np.transpose(q1))[:,0], np.dot(q1, np.transpose(q1))[:,1]))])
q2_v = np.transpose([np.hstack((np.dot(q2, np.transpose(q2))[:,0], np.dot(q2, np.transpose(q2))[:,1]))])
q3_v = np.transpose([np.hstack((np.dot(q3, np.transpose(q3))[:,0], np.dot(q3, np.transpose(q3))[:,1]))])
Y = np.hstack((q1_v, q2_v, q3_v))
print("Y:")
print(Y)
b = [1, 0, 0, 1]
# print(np.linalg.matrix_rank(Y))
# print(Y)
# print(np.linalg.inv(Y))
# print(np.linalg.solve(Y, b))
# 1/0
# Approximate solution to Y*a=b using least squares method
solution = np.dot( np.dot(np.linalg.inv(np.dot(np.transpose(Y), Y)), np.transpose(Y)) , [1, 0, 0, 1]  )
a1 = round(solution[0], 3)
a2 = round(solution[1], 3)
a3 = round(solution[2], 3)

print(a1, a2, a3)

mu1 = sqrt(a1) * q1
mu2 = sqrt(a2) * q2
mu3 = sqrt(a3) * q3

print("== Measurement vectors ==")
print("mu1: ")
print(mu1)
print("mu2: ")
print(mu2)
print("mu3: ")
print(mu3)

pi1 = np.dot(mu1, np.transpose(mu1))
pi2 = np.dot(mu2, np.transpose(mu2))
pi3 = np.dot(mu3, np.transpose(mu3))
print()
print("== Optimal measurement operators ==")
print("PI_1: ")
print(pi1)
print("PI_2: ")
print(pi2)
print("PI_3: ")
print(pi3)

print("== Norm values ==")
print("|mu1|: ")
print(norm(mu1))
print("|mu2|: ")
print(norm(mu2))
print("|mu2|: ")
print(norm(mu3))

# mu = np.hstack((mu1, mu2, mu3))
# phi = np.hstack((psi_1, psi_2, psi_3))
# print("== Matrix Mu ==")
# print(mu)
# error = np.trace(np.dot(np.matrix(phi - mu).getH(), (phi - mu)))
# print("Squared error = " + str(error))

''' Check that pi1, pi2 and pi3 check the conditions given in the paper '''
print()
print("== Solution validity check ==")
# Sum of PI_i = Identity
print(pi1 + pi2 + pi3)
# (X_sol - pi')PI_i = 0
print(np.dot(X_sol - rho_1prime, pi1))
print(np.dot(X_sol - rho_2prime, pi2))
print(np.dot(X_sol - rho_3prime, pi3))