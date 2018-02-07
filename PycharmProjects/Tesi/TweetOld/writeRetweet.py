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
        retweet = []

        def __init__(self,posizione,retweet):
                self.posizione=posizione
                self.retweet=retweet

        def makeRetweet(posizione,ret):
                retweet= Retweet()
                retweet.posizione=posizione
                retweet.retweet=ret
                return retweet




def getRetweet(api,file,lenFile,pos,list_ret):

    #row[1] contiene l'id del post

    if(pos == lenFile ):
        return list_ret
    else:

        with open(file, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in itertools.islice(reader, pos, lenFile):
                try:
                    if row[2] == '0':
                        pos = pos + 1
                        ret = Retweet(pos,'')
                        #p=ret.makeRetweet(pos,'')
                        list_ret.append(ret)
                        #list_ret.append({'pos':pos,'retweet':''})
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

                        p=Retweet(pos,temp)
                        list_ret.append(p)
                except tweepy.TweepError:
                    print('exception raised, waiting 15 minutes')
                    print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
                    time.sleep(15 * 60)
                    #return getRetweet(api,file,lenFile,pos,list_ret)
                    break

        return getRetweet(api,file,lenFile,pos,list_ret)


def main():

    with open('sampleTweets.csv') as f:
        lunghezzaFile=sum(1 for _ in f)

    print("lunghezzaFile"+str(lunghezzaFile))
    print (sys.getrecursionlimit())
    sys.setrecursionlimit(10000)


    api =connectApi.loginApi()

    list_ret = []
    result = getRetweet(api,'sampleTweets.csv',lunghezzaFile,0,list_ret)

    thefile = open('retweet.txt', 'w')

    #for item in result:
    #    thefile.write("%s\n" % item)

    for item in result:
        thefile.write(str(item.posizione) + "," + str(item.retweet)+'\n')

    print('finito',str(result))



if __name__ == '__main__':
    main()

