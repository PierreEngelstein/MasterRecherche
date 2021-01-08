import numpy as np
import math
import matplotlib.pyplot as plt
import random

n = 8
N = 2**n
n_opti = (math.pi/4)*math.sqrt(N)
nb_iter = math.floor(n_opti)
# nb_iter = 1000

w = np.zeros((N, 1))
w[random.randint(-1, N)] = np.imag(0 + 1j)

s = np.ones((N, 1)) / math.sqrt(N)
u_w = np.identity(N) - 2 * w * np.transpose(w)
u_s = 2 * s * np.transpose(s) - np.identity(N)
g = np.dot(u_s, u_w)
x = s
# print(s)
for i in range(0, nb_iter):
    x = np.dot(g, x)
    # print(x)
print(x)
# print(g)
1/0

vect_in = np.matrix([[0], [1]])
grover = np.matrix([[1, 2/math.sqrt(N)], [-2/math.sqrt(N), (N-4)/N]])
print(np.linalg.eigvals(grover))
print(np.linalg.norm(np.linalg.eigvals(grover)[1]))
print(np.dot(np.transpose(grover), grover))


values_s = []
values_w = []
values_tot = []

_2d_values = []
for i in range(0, nb_iter):
    values_w.append(vect_in.take(0).item())
    values_s.append(vect_in.take(1).item())
    _2d_values.append([vect_in.take(0).item(), vect_in.take(1).item()])
    values_tot.append(vect_in.take(0).item()**2 + vect_in.take(1).item()**2)
    vect_in = np.dot(grover, vect_in)

# Todo: tracer cercle unité

plt.plot(range(0, nb_iter), values_s, 'r--', label="|s>")
plt.plot(range(0, nb_iter), values_w, 'b--', label="|w>") 
plt.plot(range(0, nb_iter), values_tot, 'g--', label="a²+b²")

plt.scatter(values_s, values_w)

plt.legend(loc="lower right")
plt.show()