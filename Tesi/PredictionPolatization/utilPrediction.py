import pickle
import csv

with open('../Test/Biotestamento/Dicembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    labelPolRand = pickle.load(input)

with open('../Test/Biotestamento/Dicembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    labelPolVen = pickle.load(input)


myData =[]
with open('../Test/Biotestamento/Settembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    DizionarioSettembreRW = pickle.load(input)

with open('../Test/Biotestamento/Ottobre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    DizionarioOttobreRW = pickle.load(input)

with open('../Test/Biotestamento/Novembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    DizionarioNovembreRW = pickle.load(input)

with open('../Test/Biotestamento/Settembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    DizionarioSettembreV = pickle.load(input)

with open('../Test/Biotestamento/Ottobre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    DizionarioOttobreV = pickle.load(input)

with open('../Test/Biotestamento/Novembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    DizionarioNovembreV = pickle.load(input)




myFile = open('../Test/Biotestamento/testing.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    r = ["Nodo" ,"Random Walk Settembre" ,"Venezuela Settembre", "Random Walk Ottobre",
         "Venezuela Ottobre" ,"Random Walk Novembre" ,"Venezuela Novembre" ,"Random Walk Dicembre",
         "Venezuela Dicembre"]
    writer.writerow(r)
    for i in labelPolRand:
        # print i , labelPolRand[i]
        setRw = ""
        setV = ""
        ottRw = ""
        ottV = ""
        novRw = ""
        novV = ""
        if i in DizionarioSettembreRW:
            setRw = DizionarioSettembreRW[i]
        if i in DizionarioSettembreV:
            setV = DizionarioSettembreV[i]
        if i in DizionarioOttobreRW:
            ottRw = DizionarioOttobreRW[i]
        if i in DizionarioOttobreV:
            ottV = DizionarioOttobreV[i]
        if i in DizionarioNovembreRW:
            novRw = DizionarioNovembreRW[i]
        if i in DizionarioNovembreV:
            novV = DizionarioNovembreV[i]

        row = [i, setRw, setV, ottRw, ottV, novRw, novV, labelPolRand[i], labelPolVen[i]]
        myData.append(row)

    writer.writerows(myData)

print("Writing complete")
