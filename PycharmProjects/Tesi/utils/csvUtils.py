import csv

def datamonth(path):

    Dizionario={}
    with open(path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        next(readCSV, None)
        pos=0
        for row in readCSV:
            # if row[1] not in(None,"") and row[2] not in (None,""):
            #    Dizionario[pos]=row
            #    pos = pos+1
            # elif row[1] in (None,"")   and row[2] not in (None,""):
            #     Dizionario[pos] = row
            #     pos +1
            # else:
            #     continue
            if row[1] == '' or row[1] == None:

               if row[2] == '' or row[2]== None:
                   continue
               else:
                   Dizionario[pos]=row
                   pos = pos +1

            else:
                Dizionario[pos]= row
                pos = pos +1


    print pos
    return  Dizionario

def writeCsv(Dizionario,path,name):
    myData = []
    myFileWavgv = open(path, 'w')
    with myFileWavgv:
        writer = csv.writer(myFileWavgv)
        r = ["Nodo", name+" Settembre", name+" Ottobre",
             name+" Novembre", name+" Dicembre", name+" Dicembre Predetto", name+"errore"]
        writer.writerow(r)
        for i in Dizionario:
            elemento= Dizionario[i]
            row=[elemento[0],elemento[1],elemento[2],elemento[3],elemento[4],elemento[5],elemento[6]]
            myData.append(row)

        writer.writerows(myData)


def main():
    #l[0] numero Blue, l[1] numero rossi, l[2] numero grigi, l[3] totale
    l= datamonth('../Test/Biotestamento/predictionVenezuelaWindowAvg.csv')
    print l

    writeCsv(l,"./BiotestamentoCsv/predictionWindowAvgVenezuela.csv","Venezuela")



if __name__ == '__main__':
    main()