from math import log, exp

# y = -0.2
# x = exp(-1)
# x = 0.77

# it = 0
# x_prev = x
# x = x - (x*log(x) - y)/(log(x) + 1)
# print(x, x*log(x))
# it += 1
# while (abs(x_prev - x) >= 1e-15):
#     x_prev = x
#     x = x - (x*log(x) - y)/(log(x) + 1)
#     print(x, x*log(x))
#     it += 1
# print(it)


import cvxpy as cp
X = cp.Variable((2, 2), symmetric=True)
constraints = [X >> 0]
pb = cp.Problem(cp.Minimize(cp.trace(X) * cp.log(cp.trace(X))), constraints)
pb.solve()
X_sol = X.value