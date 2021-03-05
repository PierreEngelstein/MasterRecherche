'''
    A test for quantum annealing. Doesn't actually run, just translation of pseudo code found in 
    https://www.researchgate.net/publication/51914898_An_introduction_to_quantum_annealing (page 13)
'''

def cost(condition):
    # TODO
    return None

def QuantumTransition(condition, chain_length, neighbours):
    for k in neighbours:
        wave_func(k)
    # Returns the best neighbour by probability of wave function
    return best_of_neighbourgs

def LocalOptimization(epsilon):
    # TODO
    return None

def QuantumAnnealing(init, nu, tmax, tdrill, tloc):
    t = 0
    e = init
    vmin = cost(e)

    while t < tmax:
        j = 0
        while True:
            i = 0
            while True:
                e = QuantumTransition(e, nu, max)
                if cost(e) < vmin:
                    vmin = cost(e)
                    i, j = 0, 0
                else:
                    i += 1
                if i > tloc: break
            
            epsilon = LocalOptimization(e)
            if cost(e) < vmin:
                vmin = cost(e)
                j = 0

            if j < tdrill: break