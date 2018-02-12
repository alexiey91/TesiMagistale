import pickle
import csv

'''
Script for create the Prediction file for Biotestament
'''
with open('../Test/Biotestamento/Gennaio/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    labelPolRand = pickle.load(input)

with open('../Test/Biotestamento/Gennaio/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
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

with open('../Test/Biotestamento/Dicembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    DizionarioDicembreRW = pickle.load(input)

with open('../Test/Biotestamento/Dicembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    DizionarioDicembreV = pickle.load(input)


#with open('../Test/Biotestamento/14Dicembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    Dizionario14DicembreRW = {}

with open('../Test/Biotestamento/14Dicembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    Dizionario14DicembreV = pickle.load(input)


myFile = open('../Test/Biotestamento/testingUpdate.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    r = ["Nodo" ,"Random Walk Settembre" ,"Venezuela Settembre", "Random Walk Ottobre",
         "Venezuela Ottobre" ,"Random Walk Novembre" ,"Venezuela Novembre" ,"Random Walk 14Dicembre",
         "Venezuela 14Dicembre" ,"Random Walk Dicembre",
         "Venezuela Dicembre","Random Walk Gennaio",
         "Venezuela Gennaio"]
    writer.writerow(r)
    for i in labelPolRand:
        # print i , labelPolRand[i]
        setRw = ""
        setV = ""
        ottRw = ""
        ottV = ""
        novRw = ""
        novV = ""
        dic14Rw = ""
        dic14V = ""
        dicRw= ""
        dicV = ""
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

        # if i in Dizionario14DicembreRW:
        #      dic14Rw = Dizionario14DicembreRW[i]
        if i in Dizionario14DicembreV:
            dic14V = Dizionario14DicembreV[i]
        if i in DizionarioDicembreRW:
            dicRw = DizionarioDicembreRW[i]
        if i in DizionarioDicembreV:
            dicV= DizionarioDicembreV[i]

        row = [i, setRw, setV, ottRw, ottV, novRw, novV, dic14Rw,dic14V,dicRw,dicV,labelPolRand[i], labelPolVen[i]]
        myData.append(row)

    writer.writerows(myData)

print("Writing complete")
