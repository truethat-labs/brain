import pdb
import pandas as pd
import scipy
import numpy as np
import tensorflow as tf

from tensorflow import keras
from sklearn.preprocessing import normalize
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# pdb.set_trace()

data = pd.read_csv(
    'data/backtest/bank_nifty_golden_ratio(1%)_modified_with_PL.csv', usecols=[13, 14, 15, 16])
result = pd.read_csv(
    'data/backtest/bank_nifty_golden_ratio(1%)_modified_with_PL.csv', usecols=[12])

results = np.array(result).flatten()

dataArr = np.array(data)
resultArr = results[0:-1]

ninputX = normalize(dataArr.reshape(dataArr.shape[0], -1), norm='max', axis=0).reshape(dataArr.shape)
inputy = normalize(resultArr.reshape(
    resultArr.shape[0], -1), norm='max', axis=0).reshape(resultArr.shape)

# pdb.set_trace()

inputX = ninputX[:-1]
today = ninputX[725]

dataset = pd.DataFrame(inputX)
labels = pd.Series(inputy)

training_set = dataset[0:482]
test_set = dataset[483:724]
training_labels = labels[0:482]
test_labels = labels[483:724]

# Initialize our classifier
gnb = GaussianNB()

# Train our classifier
model = gnb.fit(training_set, training_labels)

# Make predictions
preds = gnb.predict(test_set)

# Evaluate accuracy
print(accuracy_score(test_labels, preds))

print('Today: ' +
      (gnb.predict(np.array([today]))[0] == 1.0 and 'Profit' or 'Loss'))
