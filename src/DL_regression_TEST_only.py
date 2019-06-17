# python DL_regression.py

# import the necessary packages
from keras.optimizers        import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing   import LabelBinarizer
from keras.models            import Sequential
from keras.models            import Model
from keras.layers.core       import Activation
from keras.layers.core       import Dropout
from keras.layers.core       import Dense

import tensorflow as tf
import pandas as pd
import numpy as np
import argparse
import locale
import keras
import glob
import cv2


# import os
# print os.getcwd()  # Prints the current working directory
#
inputPath = '../data/testing_for_DL_01.csv'

# Load dataset into DataFrame
# cols = ["geo6", "day", "hour", "min", "demand"]
cols = ["geo6", "day", "hour", "min"]
df = pd.read_csv( inputPath, sep=" ", header=None, names=cols )

# Continuous Attributes
continuous = ["day", "hour", "min"]
testContinuous  = test[continuous]

print("Info: converting categorical attributes to one-hot encoding...")
# Categorical attribute:   geohash6:
geoBinarizer = LabelBinarizer().fit( df["geo6"] )
testCategorical  = geoBinarizer.transform( test["geo6"] )

# Concatenate CATEGORICAL attributes with CONTINUOUS attributes
testX  = np.hstack( [ testCategorical,  testContinuous  ] )



#
#  READING model
#
from keras.models import load_model
model=load_model('01_model_traffic.hdf5')
#


print("Info: Starting Prediction...")
preds = model.predict( testX )

print( preds.flatten() )


## Create RMSE
#diff = preds.flatten() - testY
#percentDiff = (diff / testY) * 100
#absPercentDiff = np.abs(percentDiff)

#mean = np.mean(absPercentDiff)
## std = np.std(absPercentDiff)

## RMSE -- Root Mean Square Error:
#diff = preds.flatten() - testY
#rmse = (( preds.flatten() - testY ) ** 2).mean() ** .5
##
#locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
#print("RMSE of Ride Demand is: {}".format( rmse ) )

