from sklearn.svm import SVC
from sklearn import datasets, svm
from scipy import misc
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
import numpy
import os

healthy = []
types = []
k = 0
for file in os.listdir("Healthy/"):
    gray_matrix = imread("Healthy/" + file)
    values=[]
    for i in range(0, gray_matrix.shape[1]):
        mean = 0
        for j in range(0, gray_matrix.shape[0]):
            mean += gray_matrix[j][i]
        mean /= gray_matrix.shape[0]
        values.append(mean)
    # Add the x - y - z values to the data
    filename_splitted = file.split(".")[0].split("_")
    values.append(int(filename_splitted[0])) # Patient number
    values.append(int(filename_splitted[1])) # x
    values.append(int(filename_splitted[2])) # y
    values.append(int(filename_splitted[3])) # z
    values.append(0) # Class
    healthy.append(values)
    types.append(0)
    if k % 100 == 0:
        print(k)
    k += 1
    # if(len(healthy) == 2000): break
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
    # Add the x - y - z values to the data
    filename_splitted = file.split(".")[0].split("_")
    values.append(int(filename_splitted[0])) # Patient number
    values.append(int(filename_splitted[1])) # x
    values.append(int(filename_splitted[2])) # y
    values.append(int(filename_splitted[3])) # z
    values.append(1) # Class
    healthy.append(values)
    types.append(1)
    if k % 100 == 0:
        print(k)
    k += 1
    # if(len(healthy) == 4000): break
# numpy.savetxt("infarcted.csv", numpy.asarray(infarcted), delimiter=",")
numpy.savetxt("data.csv", numpy.asarray(healthy), delimiter=",")
numpy.savetxt("labels.csv", types, fmt='%i', delimiter=",")