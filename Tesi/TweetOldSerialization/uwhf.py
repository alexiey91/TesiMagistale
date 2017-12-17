import sys,os
import unidecode as u
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import SentimentAnalysis.test as sentiment
dizionario_hashtag = {}
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
x= '#Regionali #Sicilia . #Micari presenta listino e assessori. #Baccei all\u2019 #Economia'
x= u' '+x.encode('utf-8')
print(x)
result=sentiment.checkPartition(str(x).lower())

print result

number= divmod(401,20)

print("numeber",number," number[0]",number[0])