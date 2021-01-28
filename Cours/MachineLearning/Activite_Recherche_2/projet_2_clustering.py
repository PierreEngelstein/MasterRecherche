import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import *
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler
import sklearn.model_selection as ms
from matplotlib import pyplot as plt
import time

def equal(list1, list2):
    if len(list1) != len(list2):
        return False
    for i in range(0, len(list1)):
        if list1[i] != list2[i]:
            return False
    return True
'''
data = pd.read_csv("data.csv", header=None)
durations_random = []
changes_array_random = []
for i in range(2, 10):
    print("Executing KMeans for " + str(i) + " clusters")
    start = time.time()
    # 'init' is the method used to initialize centroids. Random: choose initial centroid center randomly; k-means++: choose in a smart way to speed up convergence.
    kmeans = KMeans(n_clusters=i, init='random').fit(data[:-4])
    durations_random.append(time.time() - start)
    # print(kmeans.labels_)

    previous_labels = None
    changes = 0
    for j in range(0, 5):
        kmeans = KMeans(n_clusters=i, init='random').fit(data[:-4])
        if previous_labels is None:
            previous_labels = kmeans.labels_
        else:
            if not equal(previous_labels, kmeans.labels_):
                changes += 1
                previous_labels = kmeans.labels_
    changes_array_random.append(changes)
    # print(str(changes) + " changes over 9 iterations." )
    score = silhouette_score(data[:-4], kmeans.labels_, metric='euclidean')
    # print("silouhette score = " + str(score))
    # print(np.min(score), np.max(score))

# durations_kmp = []
# changes_array_kmp = []
# for i in range(2, 10):
#     print("Executing KMeans for " + str(i) + " clusters")
#     start = time.time()
#     # 'init' is the method used to initialize centroids. Random: choose initial centroid center randomly; k-means++: choose in a smart way to speed up convergence.
#     kmeans = KMeans(n_clusters=i, init='k-means++').fit(data[:-4])
#     durations_kmp.append(time.time() - start)
#     # print(kmeans.labels_)

#     previous_labels = None
#     changes = 0
#     for j in range(0, 20):
#         kmeans = KMeans(n_clusters=i, init='k-means++').fit(data[:-4])
#         if previous_labels is None:
#             previous_labels = kmeans.labels_
#         else:
#             if not equal(previous_labels, kmeans.labels_):
#                 changes += 1
#                 previous_labels = kmeans.labels_
#     changes_array_kmp.append(changes)
#     # print(str(changes) + " changes over 9 iterations." )
#     score = silhouette_score(data[:-4], kmeans.labels_, metric='euclidean')
#     # print("silouhette score = " + str(score))
#     # print(np.min(score), np.max(score))


# plt.subplot(221)
# plt.plot(range(2, 10), durations_random)
# plt.subplot(222)
# plt.plot(range(2, 10), changes_array_random)
# # plt.subplot(223)
# # plt.plot(range(2, 10), durations_kmp)
# # plt.subplot(224)
# # plt.plot(range(2, 10), changes_array_kmp)
# plt.show()
'''

'''
Display clusters in 2D form, by patient, by Z axis
'''
data = pd.read_csv("data.csv", header=None)
kmeans = KMeans(n_clusters=2, init='k-means++').fit(data[:-5])
patients = {}
# print(data[:1])
for i in range(1, data.shape[0]):
    print("datas at index " + str(i))
    data_loc = data[i-1:i]
    print(data_loc)
    print(len(data_loc.values.tolist()))
    # print()
# for single_data in data:
    
# print(single_data[len(single_data) - 4])