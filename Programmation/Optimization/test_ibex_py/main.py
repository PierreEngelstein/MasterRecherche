import numpy as np
from matplotlib import pyplot as plt
from math import log

a = np.arange(0.01, 2, 0.01)
b = []
min = None
min_idx = a[0]
for i in a:
    b.append( i* log(i) )
print(min_idx, min)

plt.plot(a, b)
plt.grid()
plt.axes()
plt.show()