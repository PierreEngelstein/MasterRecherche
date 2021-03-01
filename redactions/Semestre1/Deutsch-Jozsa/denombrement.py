import math
n = 3
N = math.factorial(2**n)
R = math.factorial(2**(n-1))
D=R**2
equilibree = N/D
total = 2**(2**n)
proportion = equilibree / total
print("equilibree : " + str(equilibree))
print("total : " + str(total))
print("proportion : " + str(proportion))




