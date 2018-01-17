import numpy as np
import matplotlib.pyplot as plt

x = [1,2]
y = [0.0,0.0] # 10, not 9, so the fit isn't perfect

# fit = np.polyfit(x,y,1)
# m,q =np.polyfit(x,y,1)
# print(m)
# print(fit)
# fit_fn = np.poly1d(fit)
# print(fit_fn)
# fit_fn is now a function which takes in x and returns an estimate for y

# plt.plot(x,y, 'yo', x, fit_fn(x), '--k')
#
# plt.show()

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

