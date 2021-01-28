import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import *
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
import sklearn.model_selection as ms
from matplotlib import pyplot as plt

data = pd.read_csv("data.csv", header=None)
labels = pd.read_csv("labels.csv", header=None)

# print(data[data.columns[:-3]])

# scaler = StandardScaler()
# scaler.fit(data)
# scaled_values = scaler.transform(data)
# data = pd.DataFrame(scaled_values, index=data.index, columns=data.columns)
X_train, X_test, y_train, y_test = train_test_split(data[data.columns[:-5]], labels.values.ravel(), test_size=0.3)

print(X_train.shape)
print(X_test.shape)

clf = svm.SVC(kernel="linear")
clf.fit(X_train, y_train)

print("fitting done")
cfm = confusion_matrix(clf.predict(X_test), y_test)
print(cfm)

total = cfm[0][0] + cfm[1][0] + cfm[0][1] + cfm[1][1]
accuracy = (cfm[0][0] + cfm[1][1])/total
false_positives = cfm[0][1]/total
false_negatives = cfm[1][0]/total
errors = (cfm[0][1] + cfm[1][0])/total

print("Accuracy = " + str(accuracy))
print("False Positives = " + str(false_positives))
print("False Negatives = " + str(false_negatives))
print("Errors = " + str(errors))

# Get distance of each point to hyperplane
y_test_pred = clf.decision_function(X_test)
w_norm = np.linalg.norm(clf.coef_)
dist = y_test_pred/w_norm
print("distance from hyperplane = " + str(dist))

print("min = " + str(np.min(dist)))
print("max = " + str(np.max(dist)))

# Compute probability to be in class
min_val = np.min(dist)
max_val = np.max(dist)
values_percent = []
for i in dist:
    if i > 0:
        percent = 50 + 50*i/max_val
        values_percent.append(percent)
    if i < 0:
        i_tmp = -i
        percent = 50 + 50*i_tmp/(-min_val)
        values_percent.append(percent)
# print(values_percent)
print(len(values_percent))

fpr, tpr, thr = roc_curve(y_test, y_test_pred)
_auc = auc(fpr, tpr)


fig= plt.figure(figsize=(6, 6))
plt.plot(fpr, tpr, '-', lw=2,label='AUC=%.2f' % _auc)
plt.xlabel('Taux de faux positifs', fontsize=16)
plt.ylabel('Taux de vrais positifs', fontsize=16)
plt.title('Courbe ROC SVM', fontsize=16)
plt.legend(loc="lower right", fontsize=14)
plt.show()