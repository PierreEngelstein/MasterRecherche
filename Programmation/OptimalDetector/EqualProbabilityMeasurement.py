from math import sqrt
import cvxpy as cp
import numpy as np

w = 1/3
psi_1 = [[1/sqrt(3.0)], [1/sqrt(3.0)], [1/sqrt(3.0)]]
psi_2 = [[1/sqrt(2.0)], [1/sqrt(2.0)], [0.0]]
psi_3 = [[0.0], [1/sqrt(2.0)], [1/sqrt(2.0)]]

phi = np.hstack((psi_1, psi_2, psi_3))

phi_chap = np.dot(phi, np.linalg.inv(np.dot(np.conjugate(np.transpose(phi)), phi  )))
# phi_chap = np.around(phi_chap, 2)
phi_1 = np.transpose([phi_chap[:,0]])
phi_2 = np.transpose([phi_chap[:,1]])
phi_3 = np.transpose([phi_chap[:,2]])
print(np.around(phi_chap, 2))
print(np.around(phi_1, 2))
print(np.around(phi_2, 2))
print(np.around(phi_3, 2))

Q1 = np.dot(phi_1, np.transpose(phi_1))
Q2 = np.dot(phi_2, np.transpose(phi_2))
Q3 = np.dot(phi_3, np.transpose(phi_3))

print(np.around(Q1, 2))
print(np.around(Q2, 2))
print(np.around(Q3, 2))

F0 = np.zeros((6, 6))
F0[0, 0] = 1
F0[1, 1] = 1
F0[2, 2] = 1
print(F0)

F1 = np.zeros((6, 6))
F2 = np.zeros((6, 6))
F3 = np.zeros((6, 6))
F_Final = np.zeros((6, 6))
for i in range(0, Q1.shape[0]):
    for j in range(0, Q1[i].shape[0]):
        F1[i][j] = -Q1[i][j]
        F2[i][j] = -Q2[i][j]
        F3[i][j] = -Q3[i][j]
F1[3][3] = 1
F2[4][4] = 1
F3[5][5] = 1
C = np.transpose([[1/3, 1/3, 1/3]])
print(C)
print(np.transpose(C))

# print(np.around(F1, 2))
# print(np.around(F2, 2))
# print(np.around(F3, 2))
import dmcp

F = cp.Variable((6, 6))
P = cp.Variable((3, 1))
C = cp.Variable((3, 1))
constraints =  [C[0, 0] == 1/3]
constraints +=  [C[1, 0] == 1/3]
constraints +=  [C[2, 0] == 1/3]
constraints += [F >= 0]
constraints += [F == F0 + P[1, 0] * F1 + P[2, 0] * F2 + P[2, 0] * F3]
prob = cp.Problem(cp.Minimize( cp.trace(cp.transpose(C) @ P)), constraints)
print(dmcp.find_minimal_sets(prob))
print(dmcp.is_dmcp(prob))
# This fails with abs() getting a NoneType
result = prob.solve(method = 'bcd', ep = 1e-5)
print(P.value)