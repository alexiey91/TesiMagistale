import tweepy
import datetime as dt
import time
import csv
import itertools
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils.CreateApi as connectApi


class Retweet (object):
        posizione = 0
        user=''
        retweet = []

        def __init__(self,posizione,user,retweet):
                self.posizione=posizione
                self.user=user
                self.retweet=retweet

        def makeRetweet(posizione,ret):
                retweet= Retweet()
                retweet.posizione=posizione
                retweet.retweet=ret
                return retweet




def getRetweet(api,file,writeFile,lenFile,pos,list_ret):

    #row[1] contiene l'id del post

    if(pos == lenFile ):
        return None
    else:

        with open(file, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in itertools.islice(reader, pos, lenFile):
                try:
                    if row[2] == '0':
                        pos = pos + 1
                        ret = Retweet(pos,row[0],'')
                        #p=ret.makeRetweet(pos,'')
                        list_ret.append(ret)
                        #list_ret.append({'pos':pos,'retweet':''})
                        #writeFile.write(str(ret.posizione) + "," + str(ret.retweet) + '\n')
                        print("pos="+str(pos))

                    else:
                        results = api.retweets(row[1])
                        pos = pos + 1
                        #ret= Retweet()
                        temp = []
                        for tweet in results:
                                #p=ret.makeRetweet(pos,tweet.user.id)
                                temp.append(tweet.user.id)
                                print ("id=", tweet.user.id, " pos=", str(pos))

                        #list_ret.append({'pos':pos,'retweet':temp})

                        p=Retweet(pos,row[0],temp)
                        list_ret.append(p)
                        #writeFile.write(str(p.posizione) + "," + str(p.retweet) + '\n')
                except tweepy.TweepError:
                    print('exception raised, waiting 15 minutes')
                    print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
                    for x in range(len(list_ret)):
                        print('.')
                        writeFile.write(str(list_ret[x].posizione) + "," + list_ret[x].user + "," + str(list_ret[x].retweet) + '\n')
                    print('scrivo prima dello sleep')

                    list_ret = []
                    print("clear"+str(len(list_ret)))
                    time.sleep(15 * 60)
                    #return getRetweet(api,file,lenFile,pos,list_ret)
                    break

        return getRetweet(api,file,writeFile,lenFile,pos,list_ret)


def main():

    with open('RegionaliSicilia.csv') as f:
        lunghezzaFile=sum(1 for _ in f)

    api = connectApi.loginApi()
    list_ret = []
    thefile = open('retweet2.txt', 'a')
    try:
         getRetweet(api,'RegionaliSicilia.csv',thefile,lunghezzaFile,0,list_ret)

    except RuntimeError:
        print('Eccezione Ricorsione')
        with open('retweet2.txt') as f:
         lunghezzaRetweet = sum(1 for _ in f)
        thefile.close()
        print("Lunghezza Fil Retweet"+str(lunghezzaRetweet))
        if(lunghezzaRetweet < lunghezzaFile):
            print('Eseguo di nuovo la get Retweet, ultima tupla analizzata:'+str(lunghezzaRetweet))
            thefile = open('retweet2.txt', 'a')
            getRetweet(api, 'RegionaliSicilia.csv', thefile, lunghezzaFile, lunghezzaRetweet,list_ret)
        else:
            print('Terminato')
        #for item in result:
    #    thefile.write("%s\n" % item)

    #for item in result:
    #    thefile.write(str(item.posizione) + "," + str(item.retweet)+'\n')

    #print('finito',str(result))



if __name__ == '__main__':
    main()

