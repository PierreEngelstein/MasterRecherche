import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import *
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
import sklearn.model_selection as ms
import matplotlib as plt

data = pd.read_csv("data.csv", header=None)
labels = pd.read_csv("labels.csv", header=None)

# scaler = StandardScaler()
# scaler.fit(data)
# scaled_values = scaler.transform(data)
# data = pd.DataFrame(scaled_values, index=data.index, columns=data.columns)
X_train, X_test, y_train, y_test = train_test_split(data, labels.values.ravel(), test_size=0.2)

clf = svm.SVC(kernel="linear")
clf.fit(data, labels)

print("fitting done")
# print(clf.score(clf.predict(X_test), y_test))
cfm = confusion_matrix(clf.predict(data), labels)
print(confusion_matrix(clf.predict(data), labels))

total = cfm[0][0] + cfm[1][0] + cfm[0][1] + cfm[1][1]
accuracy = (cfm[0][0] + cfm[1][1])/total
false_positives = cfm[0][1]/total
false_negatives = cfm[1][0]/total
errors = (cfm[0][1] + cfm[1][0])/total

w = clf.coef_[0]

y_test_pred = clf.decision_function(data)

print(len(y_test_pred))


fpr, tpr, thr = roc_curve(labels, y_test_pred)
_auc = auc(fpr, tpr)

from matplotlib import pyplot as plt
fig= plt.figure(figsize=(6, 6))
plt.plot(fpr, tpr, '-', lw=2,label='AUC=%.2f' % _auc)
plt.xlabel('Taux de faux positifs', fontsize=16)
plt.ylabel('Taux de vrais positifs', fontsize=16)
plt.title('Courbe ROC SVM', fontsize=16)
plt.legend(loc="lower right", fontsize=14)
plt.show()


# print("accuracy = " + str(accuracy))
# print("false positives = " + str(false_positives))
# print("false negatives = " + str(false_negatives))
# print("error = " + str(errors))