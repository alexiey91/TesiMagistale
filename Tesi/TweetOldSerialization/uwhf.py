import sys,os
import unidecode as u
import  numpy as np
import random
import networkx as nx
import operator
import math
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
from sklearn.linear_model import LinearRegression



import csv
from dateutil import parser
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import SentimentAnalysis.test as sentiment
dizionario_hashtag = {}

class Retweet(object):
    user = ''
    retweet = []
    text=''
    date = ''

    def __init__(self, user, retweet,date):
        self.user = user
        self.retweet = retweet

        self.date = date

# with open('/home/alessandro/PycharmProjects/Tesi/utils/ListaHashtag.txt', 'r') as fileHashtags:
#
#    for line in fileHashtags:
#        if not dizionario_hashtag.has_key(line.strip()):
#                dizionario_hashtag[line] = '#'+line.strip().lower()
#
#
# lista_hash='#Rezi #CIaone #olae'
#
# x=lista_hash.strip().lower().split(" ")
# print(x)
#
# b3 = [val for val in x if val in dizionario_hashtag.values()]
#
# if len(b3)== 0:
#     print('Nessuno')
# else:
#     print('Trovato')
#
# stringa = '#Regionali #Sicilia , #Micari :Abbiamo le liste migliori, terrorizzato all\u2019idea di un esecutivo di destra con #Salvini'
# s=u''+stringa
# #stringa.encode("utf-8")
# #print(stringa)
#
# print(u._unidecode(s))x
# x= '#Palermo - 15 Dicembre Nello #Musumeci #Diventer\xe0Bellissima #Sicilia2017 #elesicilia #regionali2017 #Sicilia #13Dicembre pic.twitter.com/Zcir1ttkZ3'
# #x= u' '+x.encode('utf-8')
# #print(x)
# result=sentiment.checkPartition(str(x).lower())
#
# print result


aa_milne_arr = ['pooh']
print "np=",np.random.choice(aa_milne_arr,1, p=[1.0])[0]

neighbors = ['ciao','cane','ola']
random_num = random.randint(0,len(aa_milne_arr)-1 );
starting_node = aa_milne_arr[random_num];
print(random_num,"nodo=",starting_node)


# with open('../TweetOldSerialization/pickle/ElezioniSiciliaGraph/probRetBlue.pkl', 'rb') as input:
#     probRetBlue = pickle.load(input)
#
#
# for i in probRetBlue:
#     print probRetBlue[i]
# arrProb = [0.33, 1.0]
#
# if sum(arrProb) < 1.0:
#     arrProb[len(arrProb) - 1] = arrProb[len(arrProb) - 1] + (1 - sum(arrProb))
#
# elif sum(arrProb) > 1.0:
#     index, value = max(enumerate(arrProb), key=operator.itemgetter(1))
#     somma = 0.
#     for i in range(0, len(arrProb)):
#         if i != index:
#             somma = somma + arrProb[i]
#
#     arrProb[index] = 1 - somma

G = nx.read_gpickle("../Test/Sicilia/Dicembre/grafoSiciliaVen.pickle")

print len(G.nodes())

with open('../Test/Sicilia/Dicembre/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
    labelPol = pickle.load(input)
with open('../Test/Sicilia/Dicembre/listaColoriPolarizzazioneVenezuela.pickle', "rb") as input:
    colorNode = pickle.load(input)

    for i in labelPol:
        labelPol[i]=""
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, G.nodes(), node_size=50, with_labels=True, node_color=colorNode)

nx.draw_networkx_edges(G, pos, edge_color='g')

nx.draw_networkx_labels(G, pos, labelPol, font_size=8)
plt.savefig("../Test/Sicilia/Image/Venezuela/DicembreVenezuela.png", format="PNG")
plt.show()

# print( parser.parse("2017-09-01"))
# if parser.parse("2017-09-01") < parser.parse("2017-10-01"):
#     print "ciao"
#
# with open('../Test/Sicilia/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
#      labelPolRand = pickle.load(input)
#
# with open('../Test/Sicilia/dizionarioPolarizzazioneVenezuela.pickle', "rb") as input:
#     labelPolVen = pickle.load(input)


# myData=[]
# DizionarioDicembreVenezuela={}
# DizionarioDicembreV={}
# DizionarioDicembreVenezuela={}
# DizionarioDicembreV={}
# DizionarioDicembreVenezuela={}
# DizionarioDicembreV={}
#
#
# myFile = open('../Test/Sicilia/prova.csv', 'w')
# with myFile:
#     writer = csv.writer(myFile)
#     r = ["Nodo","Random Walk Dicembre","Venezuela Dicembre", "Random Walk Dicembre",
#          "Venezuela Dicembre","Random Walk Dicembre","Venezuela Dicembre" ,"Random Walk Dicembre","Venezuela Dicembre"]
#     writer.writerow(r)
#     for i in labelPolRand:
#         #print i , labelPolRand[i]
#         setVenezuela =""
#         setV=""
#         ottVenezuela=""
#         ottV=""
#         novVenezuela=""
#         novV=""
#         if i in DizionarioDicembreVenezuela:
#             setVenezuela= DizionarioDicembreVenezuela[i]
#         if i in DizionarioDicembreV:
#             setV= DizionarioDicembreV[i]
#         if i in DizionarioDicembreVenezuela:
#             ottVenezuela= DizionarioDicembreVenezuela[i]
#         if i in DizionarioDicembreV:
#             ottV= DizionarioDicembreV[i]
#         if i in DizionarioDicembreVenezuela:
#             novVenezuela= DizionarioDicembreVenezuela[i]
#         if i in DizionarioDicembreV:
#             novV= DizionarioDicembreV[i]
#
#         row=[i,setVenezuela,setV,ottVenezuela,ottV,novVenezuela,novV,labelPolRand[i],labelPolVen[i]]
#         myData.append(row)
#
#     writer.writerows(myData)
#
# print("Writing complete")


# def double_exponential_smoothing(series, alpha, beta):
#     result = [series[0]]
#     for n in range(1, len(series)+1):
#         if n == 1:
#             level, trend = series[0], series[1] - series[0]
#         if n >= len(series): # we are forecasting
#           value = result[-1]
#         else:
#           value = series[n]
#         last_level, level = level, alpha*value + (1-alpha)*(level+trend)
#         trend = beta*(level-last_level) + (1-beta)*trend
#         result.append(level+trend)
#     return result
#
#
#
# '''
#     @param series: is the list of series of polarization for the single node
#     @param alpha: is the adjstment factor of exponential smoothing
#     @return the list of all polarization with the prediction for the future month
# '''
#
# def exponential_smoothing(series, alpha):
#     result = [series[0]] # first value is same as series
#     for n in range(1, len(series)):
#         result.append(alpha * series[n] + (1 - alpha) * result[n-1])
#     return result

# series = [0.9,0.01]

# print "Double", double_exponential_smoothing(series, 0.9, 0.2)
# print "Double 2", double_exponential_smoothing(series, 0.5, 0.5)
#
#
# print "Single", exponential_smoothing(series, 0.8)

# def average(serie):
#     return float(sum(serie))/len(serie)
#
# def moving_average(serie, n):
#     print serie[-n:]
#     return average(serie[-n:])
#
#
#
# SERIE = [-1.0,0.14]
#
# print moving_average(SERIE,len(SERIE)-1)