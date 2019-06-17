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
inputPath = '../data/training_for_CNN_01.csv'

# Load dataset into DataFrame
cols = ["geo6", "day", "hour", "min", "demand"]
df = pd.read_csv( inputPath, sep=" ", header=None, names=cols )


# splitting training from testing
(train, test) = train_test_split(df, test_size=0.1, random_state=26)

trainY = train["demand"]
testY = test["demand"]

# Continuous Attributes
continuous = ["day", "hour", "min", "demand"]
trainContinuous = train[continuous]
testContinuous  = test[continuous]

print("Info: converting categorical attributes to one-hot encoding...")
# Categorical attribute:   geohash6:
geoBinarizer = LabelBinarizer().fit( df["geo6"] )
trainCategorical = geoBinarizer.transform( train["geo6"] )
testCategorical  = geoBinarizer.transform( test["geo6"] )

# Concatenate CATEGORICAL attributes with CONTINUOUS attributes
trainX = np.hstack( [ trainCategorical, trainContinuous ] )
testX  = np.hstack( [ testCategorical,  testContinuous  ] )


# Create NN:
inputdim = trainX.shape[1]
#
model = Sequential()
#
model.add( Dense( 2000, input_dim=inputdim, activation="relu" ))
model.add( Dense( 1000, activation="relu" ))
model.add( Dense( 500, activation="relu" ))
model.add( Dense( 200, activation="relu" ))
model.add( Dense( 80, activation="relu" ))
model.add( Dense( 20, activation="relu" ))
#
model.add( Dense( 1, activation="linear" ))


# opt = Adam(lr=1e-3, decay=1e-3 / 200)
opt = keras.optimizers.Adadelta()
model.compile(loss="mean_squared_error", optimizer=opt )


from keras.wrappers.scikit_learn import KerasRegressor

print("Info: Started Training...")
model.fit( trainX, trainY, validation_data=(testX, testY),
          epochs=2, batch_size=500)
#          epochs=25, batch_size=500)   # 12 min per Epoch
#          epochs=50, batch_size=80)    # 44 min per Epoch
#
print("Info: Completed Training...")



#   Save Model
print("Info: Saving Model...")
model.save('01_model_traffic.hdf5')
del model

from keras.models import load_model
model=load_model('01_model_traffic.hdf5')
#



print("Info: Starting Prediction...")
preds = model.predict( testX )

# Create RMSE
diff = preds.flatten() - testY
percentDiff = (diff / testY) * 100
absPercentDiff = np.abs(percentDiff)

mean = np.mean(absPercentDiff)
# std = np.std(absPercentDiff)

# RMSE -- Root Mean Square Error:
diff = preds.flatten() - testY
rmse = (( preds.flatten() - testY ) ** 2).mean() ** .5
#
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
print("RMSE of Ride Demand is: {}".format( rmse ) )

