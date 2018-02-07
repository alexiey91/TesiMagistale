import matplotlib
#matplotlib.use('GTKAgg')

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import datasets, linear_model
import pandas as pd

# Load CSV and columns
df = pd.read_csv("testLin.csv")

Y = df['x']
X = df['y']

X = X.reshape(len(X), 1)
Y = Y.reshape(len(Y), 1)

# Split the data into training/testing sets
#X_train = X[:-250]
#X_test = X[-250:]
X_train = X[:-3]
X_test = X[-3:]

# Split the targets into training/testing sets
# Y_train = Y[:-250]
# Y_test = Y[-250:]
Y_train = Y[:-3]
Y_test = Y[-3:]
print Y_train
# Plot outputs
# plt.scatter(X_test, Y_test, color='black')
# plt.title('Test Data')
# plt.xlabel('Size')
# plt.ylabel('Price')
# plt.xticks(())
# plt.yticks(())
#
# regr = linear_model.LinearRegression()
#
# # Train the model using the training sets
# x= regr.fit(X_train, Y_train)
#
#
# # Plot outputs
# plt.plot(X_test, regr.predict(X_test), color='red', linewidth=3)
# print regr.predict(X_test)
# prediction= regr.predict(5)
#
# print( str(round(regr.predict(5))) )
# plt.show()

a = X  # put your dates in here
b = Y
model = LinearRegression()
model.fit(a, b)

a_predict = [[4]]  # put the dates of which you want to predict kwh here
b_predict = model.predict(a_predict)

print b_predict