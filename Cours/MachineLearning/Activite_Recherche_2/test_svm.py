from sklearn.svm import SVC
from sklearn import datasets, svm
from scipy import misc
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
import numpy

import os
healthy = []
types = []
for file in os.listdir("Healthy/"):
    gray_matrix = imread("Healthy/" + file)
    values=[]
    for i in range(0, gray_matrix.shape[1]):
        mean = 0
        for j in range(0, gray_matrix.shape[0]):
            mean += gray_matrix[j][i]
        mean /= gray_matrix.shape[0]
        values.append(mean)
    healthy.append(values)
    types.append(0)
    if(len(healthy) == 2000): break
# numpy.savetxt("healthy.csv", numpy.asarray(healthy), delimiter=",")

infarcted = []
for file in os.listdir("Infarcted/"):
    gray_matrix = imread("Infarcted/" + file)
    values=[]
    for i in range(0, gray_matrix.shape[1]):
        mean = 0
        for j in range(0, gray_matrix.shape[0]):
            mean += gray_matrix[j][i]
        mean /= gray_matrix.shape[0]
        values.append(mean)
    # infarcted.append(values)
    healthy.append(values)
    types.append(1)
    if(len(healthy) == 4000): break
# numpy.savetxt("infarcted.csv", numpy.asarray(infarcted), delimiter=",")
numpy.savetxt("data.csv", numpy.asarray(healthy), delimiter=",")
numpy.savetxt("labels.csv", types, fmt='%i', delimiter=",")