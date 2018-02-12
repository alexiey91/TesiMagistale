import numpy as np
import matplotlib.pyplot as plt

x = [1,2]
y = [0.0,0.0] # 10, not 9, so the fit isn't perfect

'''
param serieX: the list of X element
param serieY: the list of Y element
return the value predicted with linear regression

'''
def linear(serieX,serieY):
        predictedvalue=''
        if len(serieX)<=1:
            predictedvalue=serieY[0]

        else:
            m,q = np.polyfit(serieX, serieY, 1)
            successor = (serieX[len(serieX)-1])+1
            print m,q, successor
            predictedvalue = (m*successor)+q

        return predictedvalue


print linear(x,y)

