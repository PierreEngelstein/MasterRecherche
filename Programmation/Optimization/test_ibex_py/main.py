import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from math import log

def xlog(a):
    if a <= 0.0: return 0.0
    return a * log(a)

def MutualInfo1(a, b, P1_1, P1_2, P1_3, P2_1, P2_2, P2_3):
    return -xlog(2*P2_2*b+2*P1_2*b+P2_3*a+P2_1*a+P1_3*a+P1_1*a)+xlog(2*P2_2*b+P2_3*a+P2_1*a)-xlog(-2*P2_2*b-2*P1_2*b+P2_3*(1-a)+P2_1*(1-a)+P1_3*(1-a)+P1_1*(1-a))+xlog(-2*P2_2*b+P2_3*(1-a)+P2_1*(1-a))+xlog(2*P1_2*b+P1_3*a+P1_1*a)+xlog(-2*P1_2*b+P1_3*(1-a)+P1_1*(1-a)) + (-xlog(0.1) - xlog(0.9))

def MutualInfo2(a, b, P1_1, P1_2, P1_3, P2_1, P2_2, P2_3):
    return -xlog(2*P2_2*b+2*P1_2*b+P2_1*a+P1_1*a+0.1*P2_3+0.1*P1_3)+xlog(2*P2_2*b+P2_1*a+0.1*P2_3)-xlog(-2*P2_2*b-2*P1_2*b+P2_1*(1-a)+P1_1*(1-a)+0.9*P2_3+0.9*P1_3)+xlog(-2*P2_2*b+P2_1*(1-a)+0.9*P2_3)+xlog(2*P1_2*b+P1_1*a+0.1*P1_3)+xlog(-2*P1_2*b+P1_1*(1-a)+0.9*P1_3) + (-xlog(0.1) - xlog(0.9))

A = np.arange(0, 0.5, 0.0025)
B = np.arange(0.5, 0.55, 0.00025)[:(len(A))]
p1_1, p1_2, p1_3, p2_1, p2_2, p2_3 = 0.0111111111, 0.0314269681, 0.0888888889, 0.45, 0.45, 0.45
# p1_1, p1_2, p1_3, p2_1, p2_2, p2_3 = 0.1, 0, 0, 0.45, 0.45, 0.45
# p1_1, p1_2, p1_3, p2_1, p2_2, p2_3 = 0.1, 0, 0, 0, 0, 0.9
function = []
function1 = []
for a in A:
    for b in B:
        print("a=" + str(a) + ", b=" + str(b))
        function.append(MutualInfo1(a, b, p1_1, p1_2, p1_3, p2_1, p2_2, p2_3))
        function1.append(MutualInfo2(a, b, p1_1, p1_2, p1_3, p2_1, p2_2, p2_3))

function = np.array(function)
function = function.reshape((len(A), len(B)))

function1 = np.array(function1)
function1 = function1.reshape((len(A), len(B)))

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(A, B, function, 300, cmap='viridis', edgecolor='none')
ax.set_xlabel('A')
ax.set_ylabel('B')
ax.set_zlabel('Mutual Information')
plt.show()

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(A, B, function1, 300, cmap='viridis', edgecolor='none')
ax.set_xlabel('A')
ax.set_ylabel('B')
ax.set_zlabel('Mutual Information')
plt.show()