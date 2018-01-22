import matplotlib.pyplot as plt
import csv


def datamonth(path,month):

    list=[]
    with open(path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        next(readCSV, None)
        if month == "Settembre":
            index = 1
        elif month == "Ottobre":
            index = 2
        elif month == "Dicembre":
            index = 3
        else:
            index =4

        numberBlue=0
        numberRed= 0
        numberGrey=0
        for row in readCSV:
            if row[index]!= '':
                print(index,float(row[index]))
                if(float(row[index]) > 0.0):
                    numberBlue = numberBlue+1

                elif (float(row[index]) < 0.0):

                    numberRed = numberRed +1

                else:
                    numberGrey = numberGrey+1
            else:
                continue

    somma= numberGrey+numberBlue+numberRed
    list.append(numberBlue)
    list.append(numberRed)
    list.append(numberGrey)
    list.append(somma)

    return  list

def main():
    #l[0] numero Blue, l[1] numero rossi, l[2] numero grigi, l[3] totale
    l= datamonth('./Biotestamento/predictionVenezuela.csv',"Dicembre")
    print l

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Blue', 'Red', 'Grey'

    percentBlue = (float(l[0])/l[3])
    percentRed = (float(l[1])/l[3])
    percentGrey = (float(l[2])/l[3])
    percentBlueNor = str(round(percentBlue, 2))
    percentRedNor = str(round(percentRed, 2))
    percentGreyNor = str(round(percentGrey, 2))
    #sizes = [15, 30, 45]
    sizes = [percentBlueNor,percentRedNor,percentGreyNor]
    colors = ["Blue","Red","Grey"]
    explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90,colors= colors)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig("../Test/Biotestamento/Statistiche/Venezuela/DicembreVenezuela.png", format="PNG")

    plt.show()

if __name__ == '__main__':
    main()