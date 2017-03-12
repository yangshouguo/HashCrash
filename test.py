
from sklearn.externals import joblib
from array import array
from sklearn.linear_model import LogisticRegression
import numpy as np

x = [[24, 0, 251, 38, 20, 52, 168, 1]]
print type(x)


classifier =(joblib.load('classifier.model'))
result = classifier.predict(x)
print result[0]

