import  csv
import math
import numpy as np
import matplotlib.pyplot as plt
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

        x = result[len(result) - 1]
        if x > 1.0:
            result[len(result) - 1] = 1.0
        elif x < -1.0:
            result[len(result) - 1] = -1.0

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

def linear(serieX, serieY):
        predictedvalue = ''
        if len(serieX) <= 1:
            predictedvalue = serieY[0]

        else:
            m, q = np.polyfit(serieX, serieY, 1)
            successor = (serieX[len(serieX) - 1]) + 1
            print m, q, successor
            predictedvalue = (m * successor) + q

        if predictedvalue > 1.0:
            predictedvalue =1.0
        elif predictedvalue < -1.0:
            predictedvalue = -1.0

        return predictedvalue


'''
@param serie: list of data
@return the value of average of list
'''
def average(serie):
    return float(sum(serie))/len(serie)

'''
@param serie: list of data
@param n: the lenght of window
@return the value of moving average
'''
def moving_average(serie, n):
    print serie[-n:]
    return average(serie[-n:])

def main():

    Dizionario={}

    with open('../Test/Biotestamento/testing.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)

        for row in readCSV:
            listRw = []
            listV = []
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

    myData = []
    myFile = open('../Test/Biotestamento/predictionRw.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        r = ["Nodo", "Random Walk Settembre", "Random Walk Ottobre",
              "Random Walk Novembre",  "Random Walk Dicembre","Random Walk Dicembre Predetto","errore(percentuale)"]
        writer.writerow(r)
        for i in Dizionario:
            print  i,Dizionario[i],len(Dizionario[i][1])
            seriesRw = Dizionario[i][0]
            if len(seriesRw) == 4:
                #T2 = [map(float, x) for x in Dizionario[i][0]]
                setRw = float(seriesRw[0])
                ottRw = float(seriesRw[1])
                novRw = float(seriesRw[2])
                decRw = float(seriesRw[3])
                series=[setRw,ottRw,novRw]
                print(series)
                alpha=0.8
                beta=0.6
                predictedSeries=double_exponential_smoothing(series,alpha,beta)
                decRwPr= predictedSeries[len(predictedSeries)-1]

                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row= [i,setRw,ottRw,novRw,decRw,decRwPr,errore]
                myData.append(row)

            elif len(seriesRw) == 3:
                setRw = ""
                ottRw = float(seriesRw[0])
                novRw = float(seriesRw[1])
                decRw = float(seriesRw[2])
                series = [ottRw, novRw]
                print(series)
                alpha = 0.8
                beta = 0.6
                predictedSeries = double_exponential_smoothing(series, alpha, beta)
                decRwPr = predictedSeries[len(predictedSeries) - 1]
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row= [i,setRw,ottRw,novRw,decRw,decRwPr,errore]
                myData.append(row)

            elif len(seriesRw) == 2:
                setRw = ""
                ottRw = ""
                novRw = float(seriesRw[0])
                decRw = float(seriesRw[1])
                series = [novRw]
                print(series)
                alpha = 0.8
                beta = 0.6
                #predictedSeries = double_exponential_smoothing(series, alpha, beta)
                decRwPr = novRw
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]

                myData.append(row)

            elif len(seriesRw) == 1:
                setRw = ""
                ottRw = ""
                novRw = ""
                decRw = float(seriesRw[0])
                decRwPr = ""
                row = [i, setRw, ottRw, novRw, decRw, decRwPr,""]
                myData.append(row)

        writer.writerows(myData)
        print(myData)

    myDataVexp = []
    myFileVexp = open('../Test/Biotestamento/predictionVenezuela.csv', 'w')
    with myFileVexp:
        writer = csv.writer(myFileVexp)
        r = ["Nodo", "Venezuela Settembre", "Venezuela Ottobre",
             "Venezuela Novembre", "Venezuela Dicembre", "Venezuela Dicembre Predetto"]
        writer.writerow(r)
        for i in Dizionario:
            print  i, Dizionario[i], len(Dizionario[i][1])
            seriesRw = Dizionario[i][1]
            if len(seriesRw) == 4:
                # T2 = [map(float, x) for x in Dizionario[i][0]]
                setRw = float(seriesRw[0])
                ottRw = float(seriesRw[1])
                novRw = float(seriesRw[2])
                decRw = float(seriesRw[3])
                series = [setRw, ottRw, novRw]
                print(series)
                alpha = 0.8
                beta = 0.6
                predictedSeries = double_exponential_smoothing(series, alpha, beta)
                decRwPr = predictedSeries[len(predictedSeries) - 1]
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataVexp.append(row)

            elif len(seriesRw) == 3:
                setRw = ""
                ottRw = float(seriesRw[0])
                novRw = float(seriesRw[1])
                decRw = float(seriesRw[2])
                series = [ottRw, novRw]
                print(series)
                alpha = 0.8
                beta = 0.6
                predictedSeries = double_exponential_smoothing(series, alpha, beta)
                decRwPr = predictedSeries[len(predictedSeries) - 1]
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataVexp.append(row)

            elif len(seriesRw) == 2:
                setRw = ""
                ottRw = ""
                novRw = float(seriesRw[0])
                decRw = float(seriesRw[1])
                series = [novRw]
                print(series)
                alpha = 0.8
                beta = 0.6
                # predictedSeries = double_exponential_smoothing(series, alpha, beta)
                decRwPr = novRw
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataVexp.append(row)

            elif len(seriesRw) == 1:
                setRw = ""
                ottRw = ""
                novRw = ""
                decRw = float(seriesRw[0])
                decRwPr = ""
                row = [i, setRw, ottRw, novRw, decRw, decRwPr,""]
                myDataVexp.append(row)

        writer.writerows(myDataVexp)
        print(myDataVexp)

    myDataL = []
    myFileL = open('../Test/Biotestamento/predictionRwLinear.csv', 'w')
    with myFileL:
        writer = csv.writer(myFileL)
        r = ["Nodo", "Random Walk Settembre", "Random Walk Ottobre",
             "Random Walk Novembre", "Random Walk Dicembre", "Random Walk Dicembre Predetto", "errore(percentuale)"]
        writer.writerow(r)
        for i in Dizionario:
            print  i, Dizionario[i], len(Dizionario[i][1])
            seriesRw = Dizionario[i][0]
            if len(seriesRw) == 4:
                # T2 = [map(float, x) for x in Dizionario[i][0]]
                setRw = float(seriesRw[0])
                ottRw = float(seriesRw[1])
                novRw = float(seriesRw[2])
                decRw = float(seriesRw[3])
                seriesY = [setRw, ottRw, novRw]
                seriesX = [1,2,3]
                print(seriesY)

                decRwPr = linear(seriesX,seriesY)

                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataL.append(row)

            elif len(seriesRw) == 3:
                setRw = ""
                ottRw = float(seriesRw[0])
                novRw = float(seriesRw[1])
                decRw = float(seriesRw[2])
                seriesY = [ottRw, novRw]
                seriesX = [1,2]
                #print(series)

                #predictedSeries = double_exponential_smoothing(series, alpha, beta)
                decRwPr = linear(seriesX,seriesY)

                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataL.append(row)

            elif len(seriesRw) == 2:
                setRw = ""
                ottRw = ""
                novRw = float(seriesRw[0])
                decRw = float(seriesRw[1])
                series = [novRw]
                print(series)
                alpha = 0.8
                beta = 0.6
                # predictedSeries = double_exponential_smoothing(series, alpha, beta)
                decRwPr = novRw
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]

                myDataL.append(row)

            elif len(seriesRw) == 1:
                setRw = ""
                ottRw = ""
                novRw = ""
                decRw = float(seriesRw[0])
                decRwPr = ""
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, ""]
                myDataL.append(row)

        writer.writerows(myDataL)
        print(myDataL)

    myDataL2 = []
    myFileL2 = open('../Test/Biotestamento/predictionVenezuelaLinear.csv', 'w')
    with myFileL2:
        writer = csv.writer(myFileL2)
        r = ["Nodo", "Venezuela Settembre", "Venezuela Ottobre",
             "Venezuela Novembre", "Venezuela Dicembre", "Venezuela Dicembre Predetto"]
        writer.writerow(r)
        for i in Dizionario:
            print  i, Dizionario[i], len(Dizionario[i][1])
            seriesRw = Dizionario[i][1]
            if len(seriesRw) == 4:
                # T2 = [map(float, x) for x in Dizionario[i][0]]
                setRw = float(seriesRw[0])
                ottRw = float(seriesRw[1])
                novRw = float(seriesRw[2])
                decRw = float(seriesRw[3])
                seriesY = [setRw, ottRw, novRw]
                seriesX = [1, 2, 3]

                #predictedSeries = double_exponential_smoothing(series, alpha, beta)
                decRwPr = linear(seriesX,seriesY)
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataL2.append(row)

            elif len(seriesRw) == 3:
                setRw = ""
                ottRw = float(seriesRw[0])
                novRw = float(seriesRw[1])
                decRw = float(seriesRw[2])
                seriesY = [ottRw, novRw]
                seriesX = [1,2]
                print seriesY,decRw
                decRwPr = linear(seriesX,seriesY)
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100

                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataL2.append(row)

            elif len(seriesRw) == 2:
                setRw = ""
                ottRw = ""
                novRw = float(seriesRw[0])
                decRw = float(seriesRw[1])
                series = [novRw]
                print(series)

                decRwPr = novRw
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataL2.append(row)

            elif len(seriesRw) == 1:
                setRw = ""
                ottRw = ""
                novRw = ""
                decRw = float(seriesRw[0])
                decRwPr = ""
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, ""]
                myDataL2.append(row)

        writer.writerows(myDataL2)
        print(myDataL2)
    #Prediction con media su finestra scorrevole
    myDataWavg = []
    myFileWavg = open('../Test/Biotestamento/predictionWindowAvgRw.csv', 'w')
    with myFileWavg:
        writer = csv.writer(myFileWavg)
        r = ["Nodo", "Random Walk Settembre", "Random Walk Ottobre",
             "Random Walk Novembre", "Random Walk Dicembre", "Random Walk Dicembre Predetto", "errore(percentuale)"]
        writer.writerow(r)
        for i in Dizionario:
            print  i, Dizionario[i], len(Dizionario[i][1])
            seriesRw = Dizionario[i][0]
            if len(seriesRw) == 4:
                # T2 = [map(float, x) for x in Dizionario[i][0]]
                setRw = float(seriesRw[0])
                ottRw = float(seriesRw[1])
                novRw = float(seriesRw[2])
                decRw = float(seriesRw[3])
                series = [setRw, ottRw, novRw]
                print(series)

                decRwPr = moving_average(series,len(series)-1)

                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataWavg.append(row)

            elif len(seriesRw) == 3:
                setRw = ""
                ottRw = float(seriesRw[0])
                novRw = float(seriesRw[1])
                decRw = float(seriesRw[2])
                series = [ottRw, novRw]

                decRwPr = moving_average(series, len(series) - 1)
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataWavg.append(row)

            elif len(seriesRw) == 2:
                setRw = ""
                ottRw = ""
                novRw = float(seriesRw[0])
                decRw = float(seriesRw[1])
                series = [novRw]

                decRwPr = novRw
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]

                myDataWavg.append(row)

            elif len(seriesRw) == 1:
                setRw = ""
                ottRw = ""
                novRw = ""
                decRw = float(seriesRw[0])
                decRwPr = ""
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, ""]
                myDataWavg.append(row)

        writer.writerows(myDataWavg)
        print(myDataWavg)

    myDataWavgv = []
    myFileWavgv = open('../Test/Biotestamento/predictionVenezuelaWindowAvg.csv', 'w')
    with myFileWavgv:
        writer = csv.writer(myFileWavgv)
        r = ["Nodo", "Venezuela Settembre", "Venezuela Ottobre",
             "Venezuela Novembre", "Venezuela Dicembre", "Venezuela Dicembre Predetto"]
        writer.writerow(r)
        for i in Dizionario:
            print  i, Dizionario[i], len(Dizionario[i][1])
            seriesRw = Dizionario[i][1]
            if len(seriesRw) == 4:
                # T2 = [map(float, x) for x in Dizionario[i][0]]
                setRw = float(seriesRw[0])
                ottRw = float(seriesRw[1])
                novRw = float(seriesRw[2])
                decRw = float(seriesRw[3])
                series = [setRw, ottRw, novRw]
                decRwPr = moving_average(series, len(series) - 1)

                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataWavgv.append(row)

            elif len(seriesRw) == 3:
                setRw = ""
                ottRw = float(seriesRw[0])
                novRw = float(seriesRw[1])
                decRw = float(seriesRw[2])
                series = [ottRw, novRw]
                decRwPr = moving_average(series, len(series) - 1)

                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataWavgv.append(row)

            elif len(seriesRw) == 2:
                setRw = ""
                ottRw = ""
                novRw = float(seriesRw[0])
                decRw = float(seriesRw[1])

                decRwPr = novRw
                if math.fabs(decRw - decRwPr) == 0:
                    errore = 0
                else:
                    errore = (math.fabs(decRw - decRwPr) / 2) * 100
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, errore]
                myDataWavgv.append(row)

            elif len(seriesRw) == 1:
                setRw = ""
                ottRw = ""
                novRw = ""
                decRw = float(seriesRw[0])
                decRwPr = ""
                row = [i, setRw, ottRw, novRw, decRw, decRwPr, ""]
                myDataWavgv.append(row)

        writer.writerows(myDataWavgv)
        print(myDataWavgv)

if __name__ == '__main__':
    main()