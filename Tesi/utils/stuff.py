import csv
import heapq
def datamonth(path,position):

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
            if row[position] == '' or row[position] == None:
                continue

            else:
                Dizionario[pos]= row[position]
                pos = pos +1


    print pos
    return  Dizionario

def writeCsv(Dizionario,path,name,month):
    myData = []
    myFileWavgv = open(path, 'w')
    with myFileWavgv:
        writer = csv.writer(myFileWavgv)
        r = [month+" "+name]
        writer.writerow(r)
        for i in Dizionario:
            elemento= Dizionario[i]
            row=[elemento]
            myData.append(row)

        writer.writerows(myData)

def writeCsvCon(Dizionario,totale,path,name,month):
    myData = []
    myFileWavgv = open(path, 'w')
    with myFileWavgv:
        writer = csv.writer(myFileWavgv)
        r = [month+" "+name,""]
        writer.writerow(r)
        r = ["totale",totale]
        writer.writerow(r)
        for i in Dizionario:
            elemento= Dizionario[i]
            row=[i,elemento]
            myData.append(row)

        writer.writerows(myData)

def writeRangeCsv(path):
    data = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    DizionarioCont={}
    for i in data:
        DizionarioCont[i]=0
    x=0
    with open(path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        next(readCSV, None)
        pos=0
        for row in readCSV:
           row= float(row[0])
           if row == -1:

               DizionarioCont[-1]= DizionarioCont[-1]+1
           elif row>-1 and row <= -0.9:
               DizionarioCont[-0.9] = DizionarioCont[-0.9] + 1
           elif row > -0.9 and row <= -0.8:
               DizionarioCont[-0.8] = DizionarioCont[-0.8] + 1
           elif row>-0.8 and row <= -0.7:
               DizionarioCont[-0.7] = DizionarioCont[-0.7] + 1
           elif row>-0.7 and row <= -0.6:
               DizionarioCont[-0.6] = DizionarioCont[-0.6] + 1
           elif row>-0.6 and row <= -0.5:
               DizionarioCont[-0.5] = DizionarioCont[-0.5] + 1
           elif row > -0.5 and row <= -0.4:
               DizionarioCont[-0.4] = DizionarioCont[-0.4] + 1
           elif row > -0.4 and row <= -0.3:
               DizionarioCont[-0.3] = DizionarioCont[-0.3] + 1
           elif row>-0.3 and row <= -0.2:
               DizionarioCont[-0.2] = DizionarioCont[-0.2] + 1
           elif row > -0.2 and row <= -0.1:
               DizionarioCont[-0.1] = DizionarioCont[-0.1] + 1
           elif row > -0.1 and row <= 0:
               DizionarioCont[0] = DizionarioCont[0] + 1
           elif row > 0 and row <= 0.1:
               DizionarioCont[0.1] = DizionarioCont[0.1] + 1
           elif row > 0.1 and row <= 0.2:
               DizionarioCont[0.2] = DizionarioCont[0.2] + 1
           elif row > 0.2 and row <= 0.3:
               DizionarioCont[0.3] = DizionarioCont[0.3] + 1
           elif row > 0.3 and row <= 0.4:
               DizionarioCont[0.4] = DizionarioCont[0.4] + 1
           elif row > 0.4 and row <= 0.5:
               DizionarioCont[0.5] = DizionarioCont[0.5] + 1
           elif row > 0.5 and row <= 0.6:
               DizionarioCont[0.6] = DizionarioCont[0.6] + 1
           elif row > 0.6 and row <= 0.7:
               DizionarioCont[0.7] = DizionarioCont[0.7] + 1
           elif row > 0.7 and row <= 0.8:
               DizionarioCont[0.8] = DizionarioCont[0.8] + 1
           elif row > 0.8 and row <= 0.9:
               DizionarioCont[0.9] = DizionarioCont[0.9] + 1
           elif row > 0.9 and row <= 1:
               DizionarioCont[1] = DizionarioCont[1] + 1
           else:
               print row
               x=x+1


    print x
    return  DizionarioCont

def main():
    #l[0] numero Blue, l[1] numero rossi, l[2] numero grigi, l[3] totale
    # l= datamonth('../Test/Sicilia/predictionRw.csv',2)
    # print l
    #
    # writeCsv(l,"./SiciliaCsv/5NovembreRw.csv","Rw","5Novembre")
    # DizionarioCon = writeRangeCsv("./SiciliaCsv/5NovembreRw.csv")
    # print DizionarioCon
    #
    # writeCsvCon(DizionarioCon,len(l),"./SiciliaCsv/ContatoriCsv/Rw/5NovembreContRw.csv","Rw","5Novembre")

    l = datamonth('../Test/Sicilia/testing5.csv', 9)
    print l

    writeCsv(l,"./SiciliaCsv/5NovembreRw.csv","Rw","5Novembre")
    DizionarioCon = writeRangeCsv("./SiciliaCsv/5NovembreRw.csv")
    print DizionarioCon

    writeCsvCon(DizionarioCon,len(l),"./SiciliaCsv/ContatoriCsv/Rw/5NovembreContRw.csv","Rw","5Novembre")
if __name__ == '__main__':
    main()