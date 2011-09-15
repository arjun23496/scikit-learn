"""
================================================
Label Propagation versus SVM on the Iris dataset
================================================

Performance comparison between Label Propagation in the semi-supervised setting
to SVM in the supervised setting in the iris dataset.

First 9 experiments: SVM (SVM), Label Propagation (LP), Label Spreading (LS)
operate in the "inductive setting". That is, the system is trained with some
percentage of data and then queried against unseen datapoints to infer a label.

The final 10th experiment is in the transductive setting. Using a label
spreading algorithm, the system is trained with approximately 24 percent of the
data labeled and during training, unlabeled points are transductively assigned
values. The test precision, recall, and F1 scores are based on these
transductively assigned labels.
"""
print __doc__

import numpy as np

from sklearn import datasets
from sklearn import svm
from sklearn import label_propagation

from sklearn.metrics.metrics import precision_score
from sklearn.metrics.metrics import recall_score
from sklearn.metrics.metrics import f1_score

rng = np.random.RandomState(0)

iris = datasets.load_iris()

X = iris.data
y = iris.target

# 80% data to keep
hold_80 = rng.rand(len(y)) < 0.8
train, = np.where(hold_80)

# 20% test data
test, = np.where(hold_80 == False)

X_all = X[train]
y_all = y[train]

svc = svm.SVC(kernel='rbf')
svc.fit(X_all, y_all)
print "Limited Label data example"
print "Test name\tprecision\trecall   \tf1"
print "SVM 80.0pct\t%0.6f\t%0.6f\t%0.6f" %\
        (precision_score(svc.predict(X[test]), y[test]),
         recall_score(svc.predict(X[test]), y[test]),
         f1_score(svc.predict(X[test]), y[test]))

print "-------"

for num in [0.2, 0.3, 0.4, 1.0]:
    lp = label_propagation.LabelPropagation()
    hold_new = rng.rand(len(train)) > num
    train_new, = np.where(hold_new)
    y_dup = np.copy(y_all)
    y_dup[train_new] = -1
    lp.fit(X_all, y_dup)
    print "LP %0.1fpct\t%0.6f\t%0.6f\t%0.6f" % \
            (80 * num, precision_score(lp.predict(X[test]), y[test]),
             recall_score(lp.predict(X[test]), y[test]),
             f1_score(lp.predict(X[test]), y[test]))

# label spreading
for num in [0.2, 0.3, 0.4, 1.0]:
    lspread = label_propagation.LabelSpreading()
    hold_new = rng.rand(len(train)) > num
    train_new, = np.where(hold_new)
    y_dup = np.copy(y_all)
    y_dup[train_new] = -1
    lspread.fit(X_all, y_dup)
    print "LS %0.1fpct\t%0.6f\t%0.6f\t%0.6f" % \
            (80 * num, precision_score(lspread.predict(X[test]), y[test]),
             recall_score(lspread.predict(X[test]), y[test]),
             f1_score(lspread.predict(X[test]), y[test]))

print "-------"
lspread = label_propagation.LabelSpreading(alpha=0.8)
y_dup = np.copy(y)
hold_new = rng.rand(len(train)) > 0.3
train_new, = np.where(hold_new)
y_dup = np.copy(y)
y_dup[train_new] = -1
lspread.fit(X, y)
trans_result = np.asarray(lspread.transduction_)
print "LS 20tran\t%0.6f\t%0.6f\t%0.6f" % \
        (precision_score(trans_result[test], y[test]),
         recall_score(trans_result[test], y[test]),
         f1_score(trans_result[test], y[test]))
