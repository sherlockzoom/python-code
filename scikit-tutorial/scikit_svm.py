#!/usr/bin/env python
# coding=utf-8
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()
clf = svm.SVC(gamma=0.0001, C=100)
x,y = digits.data[:-10], digits.target[:-10]
clf.fit(x, y)
for i in range(10):
    print ('Prediction:', clf.predict(digits.data[-i]))
    plt.imshow(digits.images[-i], cmap=plt.cm.gray_r, interpolation="nearest")
    plt.show()

