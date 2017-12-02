
import unidecode

dizionario_hashtag = {}
with open('/home/alessandro/PycharmProjects/Tesi/utils/ListaHashtag.txt', 'r') as fileHashtags:

   for line in fileHashtags:
       if not dizionario_hashtag.has_key(line.strip()):
               dizionario_hashtag[line] = '#'+line.strip().lower()


lista_hash='#Rezi #CIaone #olae'

x=lista_hash.strip().lower().split(" ")
print(x)

b3 = [val for val in x if val in dizionario_hashtag.values()]

if len(b3)== 0:
    print('Nessuno')
else:
    print('Trovato')

stringa = '#Regionali #Sicilia , #Micari :Abbiamo le liste migliori, terrorizzato all\u2019idea di un esecutivo di destra con #Salvini'

stringa.encode("utf-8")
print(stringa)
print(unidecode._unidecode(stringa))