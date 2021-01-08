import numpy as np
import math
import random
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

var_qubits = QuantumRegister(4, name='v')
clause_qubits = QuantumRegister(4, name='c')
output_qubits = QuantumRegister(1, name='out')
cbits = ClassicalRegister(4, name='cbits')
qc = QuantumCircuit(var_qubits, clause_qubits, output_qubits, cbits)
qc.initialize([1, -1]/np.sqrt(2), output_qubits)
qc.h(var_qubits)
qc.barrier()
