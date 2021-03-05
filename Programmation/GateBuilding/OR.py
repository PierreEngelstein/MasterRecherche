import numpy as np
import math
import random
from qiskit import *

def AND(circuit, a, b, control):
    circuit.h(b)
    circuit.ccx(a, b, control)

qc = QuantumCircuit(3, 3)

qc.h(0)
qc.h(1)
# qc.x(0)
# qc.x(1)
qc.x(2)
qc.cswap(0, 1, 2)
qc.barrier()
qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)

result = qiskit.visualization.circuit_drawer(qc, output="text")
print(result)

backend = BasicAer.get_backend('qasm_simulator')
shots = 1024
result = qiskit.execute(qc, backend,shots=shots).result()
counts = result.get_counts(qc)
for res in sorted(counts.int_raw):
    print("{0:03b}".format(res))
print(counts)