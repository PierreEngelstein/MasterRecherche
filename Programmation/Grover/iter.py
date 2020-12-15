import numpy as np
import math
import matplotlib.pyplot as plt

n = 16
N = 2**n
n_opti = (math.pi/4)*math.sqrt(N)
nb_iter = math.ceil(n_opti)
nb_iter = 1000

print("optimum = " + str(n_opti))

vect_in = np.matrix([[1], [0]])
grover = np.matrix([[1, 2/math.sqrt(N)], [-2/math.sqrt(N), (N-4)/N]])

values_s = []
values_w = []
values_tot = []

for i in range(0, nb_iter):
    values_w.append(vect_in.take(0).item())
    values_s.append(vect_in.take(1).item())
    values_tot.append(vect_in.take(0).item()**2 + vect_in.take(1).item()**2)
    vect_in = np.dot(grover, vect_in)

# Todo: tracer cercle unité

plt.plot(range(0, nb_iter), values_s, 'r--', label="|s>")
plt.plot(range(0, nb_iter), values_w, 'b--', label="|w>") 
plt.plot(range(0, nb_iter), values_tot, 'g--', label="a²+b²")
plt.legend(loc="lower right")
plt.show()