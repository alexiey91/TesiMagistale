import sys,os
import unidecode as u
import  numpy as np
import random
import operator
import math
import pickle
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
# x= '#Palermo - 15 settembre Nello #Musumeci #Diventer\xe0Bellissima #Sicilia2017 #elesicilia #regionali2017 #Sicilia #13settembre pic.twitter.com/Zcir1ttkZ3'
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
arrProb = [0.33, 1.0]

if sum(arrProb) < 1.0:
    arrProb[len(arrProb) - 1] = arrProb[len(arrProb) - 1] + (1 - sum(arrProb))

elif sum(arrProb) > 1.0:
    index, value = max(enumerate(arrProb), key=operator.itemgetter(1))
    somma = 0.
    for i in range(0, len(arrProb)):
        if i != index:
            somma = somma + arrProb[i]

    arrProb[index] = 1 - somma