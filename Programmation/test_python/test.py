from qiskit import QuantumRegister,ClassicalRegister,QuantumCircuit,Aer,execute
from qiskit.providers.aer import QasmSimulator
import numpy as np
from math import sqrt
# qr=QuantumRegister(1)
# cr0=ClassicalRegister(5)
# circ=QuantumCircuit(qr,cr0)
# circ.measure(qr,cr0[0])
# circ.x(qr)
# circ.measure(qr,cr0[2])
# circ.measure(qr,cr0[3])
# circ.x(qr)
# circ.measure(qr,cr0[3])
# circ.x(qr)
# circ.measure(qr,cr0[4])
# circ.h(qr)
# circ.x(qr)
# print(execute(circ,Aer.get_backend('qasm_simulator')).result().get_counts())