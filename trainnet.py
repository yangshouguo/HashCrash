
import numpy as np
from sklearn.datasets import load_iris

iris = load_iris()
samples = iris.data
target = iris.target
from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression() #use all default param


input_train = np.loadtxt("input_train.txt",delimiter = ",")
output_train = np.loadtxt("output_train.txt",delimiter = ",")
input_test = np.loadtxt("input_test.txt",delimiter = ",")
output_test = np.loadtxt("output_test.txt",delimiter = ",")

classifier.fit(input_train, output_train)
test_out = classifier.predict(input_test)
print test_out-output_test

from sklearn.externals import joblib

joblib.dump(classifier, 'classifier.model')