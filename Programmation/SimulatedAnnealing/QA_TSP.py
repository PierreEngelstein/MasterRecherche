import dwave_networkx
import networkx
import dimod
g = networkx.Graph()
g.add_weighted_edges_from({(0, 1, .1), (0, 2, .5), (0, 3, .1), (1, 2, .1),(1, 3, .5), (2, 3, .1)})

print(dwave_networkx.algorithms.traveling_salesperson(g, dimod.ExactSolver(), start=0))

'''
def int_to_bit(value: int, fix_length=-1):
    if fix_length == -1:
        return [True if value & (1 << (value.bit_length() - 1 -n)) else False for n in range(value.bit_length())]
    else:
        return [True if value & (1 << (fix_length - 1 -n)) else False for n in range(fix_length)]

def bool_func(bit_array):
    return (bit_array[0] and bit_array[1]) or (bit_array[2] and (not bit_array[1])) or (bit_array[0] and bit_array[2])

for i in range(0, 8):
    print(int_to_bit(i, 3), bool_func(int_to_bit(i, 3)))
'''

import dwavebinarycsp as dbc

and_gate = dbc.factories.and_gate(["x1", "x2", "x3"])
and_csp = dbc.ConstraintSatisfactionProblem('BINARY')
dbc.factories.multiplication_circuit(8)
and_csp.add_constraint(and_gate)
print(and_csp.check({"x1": 1, "x2": 1, "x3": 1}))

''' Structural imbalance problem '''
import dwave_networkx as dnx
import networkx as nx
import random
import dimod

G = nx.complete_graph(4)
# Randomly assign +1 or -1 relationship signs to all edges. Rename node 0 to Alice, 1 to Bob, etc
G.add_edges_from([(u, v, {'sign': 2 * random.randint(0, 1) - 1}) for u, v in G.edges])
nx.relabel_nodes(G, {0: 'Alice', 1: 'Bob', 2: 'Eve', 3: 'Wally'}, copy=False)
imbalance, bicoloring = dnx.structural_imbalance(G, dimod.ExactSolver())
for edge in G.edges:
    G.edges[edge]['frustrated'] = edge in imbalance
for node in G.nodes:
    G.nodes[node]['color'] = bicoloring[node]
print('Yellow set: \n\t' + '\n\t'.join(list(person for (person, color) in bicoloring.items() if (color == 0))))
print('Blue set: \n\t' + '\n\t'.join(list(person for (person, color) in bicoloring.items() if (color == 1))))
print('Frustrated relationships: \n\t' + '\n\t'.join(list(x + " & " + y for (x, y) in imbalance.keys())))

''' Feature selection '''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools

sig_len = 100
in1 = np.sin(np.linspace(-np.pi, np.pi, sig_len)).reshape(sig_len, 1)
in2 = np.sin(np.linspace(-np.pi + 0.1, np.pi + 0.2, sig_len)).reshape(sig_len, 1) + 0.3 * np.random.rand(sig_len, 1)
in3 = np.sin(np.linspace(-1, 1, sig_len)).reshape(sig_len, 1) + 2 * np.random.rand(sig_len, 1)
out = 2 * in1 + 3 * in2 + 6 * in3

plt.subplot(221)
plt.plot(np.linspace(-np.pi, np.pi, sig_len), in1, color="red")
plt.title("in1")
plt.subplot(222)
plt.plot(np.linspace(-np.pi + 0.1, np.pi + 0.2, sig_len), in2, color="green")
plt.title("in2")
plt.subplot(223)
plt.plot(np.linspace(-1, 1, sig_len), in3, color="blue")
plt.title("in3")
plt.subplot(224)
plt.plot(np.linspace(-np.pi, np.pi, sig_len), out, color="black")
plt.title("out")
# plt.show()

toy = pd.DataFrame(np.hstack((in1, in2, in3, out)), columns=["in1", "in2", "in3", "out"])


def two_var_model(in_tuple, a, b):
    ina, inb = in_tuple
    return a * ina + b * inb


def shannon_entropy(p):
    """Shannon entropy H(X) is the sum of P(X)log(P(X)) for probabilty distribution P(X)."""
    p = p.flatten()
    return -sum(pi * np.log2(pi) for pi in p if pi)


def conditional_shannon_entropy(p, *conditional_indices):
    """Shannon entropy of P(X) conditional on variable j"""
    axis = tuple(i for i in np.arange(len(p.shape)) if i not in conditional_indices)
    return shannon_entropy(p) - shannon_entropy(np.sum(p, axis=axis))


def mutual_information(p, j):
    """Mutual information between all variables and variable j"""
    return shannon_entropy(np.sum(p, axis=j)) - conditional_shannon_entropy(p, j)


def conditional_mutual_information(p, j, *conditional_indices):
    """Mutual information between variables X and variable Y conditional on variable Z."""
    return conditional_shannon_entropy(np.sum(p, axis=j), *conditional_indices) - conditional_shannon_entropy(p, j,
                                                                                                              *conditional_indices)


def prob(dataset, max_bins=10):
    """Joint probability distribution P(X) for the given data."""
    # bin by the number of different values per feature
    num_rows, num_columns = dataset.shape
    bins = [min(len(np.unique(dataset[:, ci])), max_bins) for ci in range(num_columns)]
    freq, _ = np.histogramdd(dataset, bins)
    p = freq / np.sum(freq)
    return p


bqm = dimod.BinaryQuadraticModel.empty(dimod.BINARY)
for column in toy.columns:
    if column == 'out':
        continue
    mi = mutual_information(prob(toy[['out', column]].values), 1)
    bqm.add_variable(column, -mi)
print("******")
for item in bqm.linear.items():
    print("{}: {:.3f}".format(item[0], item[1]))

# Quadratic coefficients ((in1,in2), (in1,in3), (in2,in3))
for f0, f1 in itertools.combinations(['in1', 'in2', 'in3'], 2):
    cmi_01 = conditional_mutual_information(prob(toy[['out', f0, f1]].values), 1, 2)
    cmi_10 = conditional_mutual_information(prob(toy[['out', f1, f0]].values), 1, 2)
    bqm.add_interaction(f0, f1, -cmi_01)
    bqm.add_interaction(f1, f0, -cmi_10)

# We want exactly k features to be selected: penalise solutions that have fewer or larger features
k = 1
bqm.update(dimod.generators.combinations(bqm.variables, k, strength=4))

bqm.normalize()

for item in bqm.quadratic.items():
    print("{}: {:.3f}".format(item[0], item[1]))
sampler = dimod.ExactSolver()
result = sampler.sample(bqm)
print(result)

print("**********")
print("**********")
''' Solving simple problem'''
import neal
''' Conversion from Ising model to QUBO model '''
qubo_from_ising = dimod.ising_to_qubo({'s1': 1, 's2': 2}, {('s1', 's2'): 5, ('s1', 's3'): 7})[0]
print(qubo_from_ising)
Q1 = {('q1', 'q1'): 0.1, ('q2', 'q2'): 0.1, ('q1', 'q2'): -0.2}
Q2 = {('q1', 'q1'): 0.5, ('q2', 'q2'): 0.5, ('q1', 'q2'): -1}
exact_sampler = dimod.ExactSolver()
sa_sampler = neal.SimulatedAnnealingSampler()
sample_set = exact_sampler.sample_qubo(Q1)
print(sample_set)
sample_set_1 = exact_sampler.sample_qubo(Q2)
print(sample_set_1)

sample_set_2 = exact_sampler.sample_qubo(qubo_from_ising)
print(sample_set_2)
sample_set_3 = sa_sampler.sample_qubo(qubo_from_ising, num_reads=5000).aggregate()
print(sample_set_3)


#s1 + 2s2 + 5s1s2 + 7s1s3
#-22x1 - 6x2 - 14x3 + 20x1x2 + 28x1x3 + 9


# -1xn
