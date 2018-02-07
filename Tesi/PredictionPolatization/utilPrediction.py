import pickle
import csv

with open('../Test/Sicilia/Dicembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    labelPolRand = pickle.load(input)

with open('../Test/Sicilia/Dicembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    labelPolVen = pickle.load(input)


myData =[]
with open('../Test/Sicilia/Settembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    DizionarioSettembreRW = pickle.load(input)

with open('../Test/Sicilia/Ottobre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    DizionarioOttobreRW = pickle.load(input)

with open('../Test/Sicilia/Novembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    DizionarioNovembreRW = pickle.load(input)

with open('../Test/Sicilia/Settembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    DizionarioSettembreV = pickle.load(input)

with open('../Test/Sicilia/Ottobre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    DizionarioOttobreV = pickle.load(input)

with open('../Test/Sicilia/Novembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    DizionarioNovembreV = pickle.load(input)


with open('../Test/Sicilia/5Novembre/dizionarioPolarizzazioneRandomWalk.pickle', "rb") as input:
    Dizionario5NovembreRW = pickle.load(input)


with open('../Test/Sicilia/5Novembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    Dizionario5NovembreV = pickle.load(input)




myFile = open('../Test/Sicilia/testing5.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    r = ["Nodo" ,"Random Walk Settembre" ,"Venezuela Settembre", "Random Walk Ottobre",
         "Venezuela Ottobre" ,"Random Walk Novembre" ,"Venezuela Novembre" ,"Random Walk Dicembre",
         "Venezuela Dicembre","Random Walk 5Novembre", "Venezuela 5Novembre"]
    writer.writerow(r)
    for i in labelPolRand:
        # print i , labelPolRand[i]
        setRw = ""
        setV = ""
        ottRw = ""
        ottV = ""
        novRw = ""
        novV = ""
        cinqueNovRw=""
        cinqueNovV = ""
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

        if i in Dizionario5NovembreRW:
            cinqueNovRw = Dizionario5NovembreRW[i]
        if i in Dizionario5NovembreV:
            cinqueNovV = Dizionario5NovembreV[i]

        row = [i, setRw, setV, ottRw, ottV, novRw, novV, labelPolRand[i], labelPolVen[i], cinqueNovRw, cinqueNovV]
        myData.append(row)

    writer.writerows(myData)

print("Writing complete")
