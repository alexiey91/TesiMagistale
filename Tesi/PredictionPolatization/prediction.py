import  csv


'''

    @param series: is the list of series of polarization for the single node
    @param alpha: is the adjstment factor of exponential smoothing
    @param beta: is the adjstment factor of trend of exponential smoothing
    @return the list of all polarization with the prediction for the future month

'''


def double_exponential_smoothing(series, alpha, beta):
    result = [series[0]]
    for n in range(1, len(series)+1):
        if n == 1:
            level, trend = series[0], series[1] - series[0]
        if n >= len(series): # we are forecasting
          value = result[-1]
        else:
          value = series[n]
        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend
        result.append(level+trend)
    return result



'''
    @param series: is the list of series of polarization for the single node
    @param alpha: is the adjstment factor of exponential smoothing
    @return the list of all polarization with the prediction for the future month
'''

def exponential_smoothing(series, alpha):
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result



def main():
    series = [-0.2, -0.15, -0.07]

    print "Double", double_exponential_smoothing(series, 0.9, 0.2)

    print "Double 2", double_exponential_smoothing(series, 0.3, 0.2)

    print "Single", exponential_smoothing(series, 0.1)

    print "Single 2", exponential_smoothing(series, 0.3)

    Dizionario={}

    with open('../Test/Sicilia/prova.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)
        listRw=[]
        listV=[]
        for row in readCSV:

            if (row[1] != ""):
                listRw.append(row[1])
            if (row[2] != ""):
                listV.append(row[2])
            if (row[3] != ""):
                listRw.append(row[3])
            if (row[4] != ""):
                listV.append(row[4])
            if (row[5] != ""):
                listRw.append(row[5])
            if (row[6] != ""):
                listV.append(row[6])
            if (row[7] != ""):
                listRw.append(row[7])
            if (row[8] != ""):
                listV.append(row[8])


            Dizionario[row[0]]=(listRw,listV)

    for i in Dizionario:
      print Dizionario[i]
      break


if __name__ == '__main__':
    main()