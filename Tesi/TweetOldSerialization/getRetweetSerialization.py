from __future__ import division
import tweepy
import datetime as dt
import time
import sys
import pickle
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils.CreateApi as connectApi

class Tweet(object):
    def __init__(self, username, tweetId, numRetweet, text, mentions, hashtags, date, link):
        self.username = username
        self.tweetId = tweetId
        self.numRetweet = numRetweet
        self.text = text
        self.mentions = mentions
        self.hashtags = hashtags
        self.date = date
        self.link = link


class countOccTweet(object):
    def __init__(self, username,count):
        self.username = username
        self.count = count

    def __str__(self):
        return self.username+" "+str(self.count)


class countOccReTweet(object):
    def __init__(self, edge, count):
        self.edge = edge
        self.count = count

    def __str__(self):
        return str(self.edge) + " " + str(self.count)


class Retweet(object):
    user = ''
    retweet = []

    def __init__(self,user, retweet):

        self.user = user
        self.retweet = retweet




def getRetweet(api,listaInput,lenLista,pos,list_ret):

    #row[1] contiene l'id del post

    if(pos == lenLista ):
        return None
    else:

        for i in range(pos,lenLista):
            try:
                if listaInput[i].numRetweet == '0':
                    pos = pos + 1
                    ret = Retweet(listaInput[i].username,'')
                    #p=ret.makeRetweet(pos,'')
                    list_ret.append(ret)
                    #list_ret.append({'pos':pos,'retweet':''})
                    #writeFile.write(str(ret.posizione) + "," + str(ret.retweet) + '\n')
                    print("pos="+str(pos))

                else:
                    results = api.retweets(listaInput[i].tweetId)
                    pos = pos + 1
                    temp = []
                    for tweet in results:
                        #p=ret.makeRetweet(pos,tweet.user.id)
                        temp.append(tweet.user.id)
                        print ("id=", tweet.user.id, " pos=", str(pos))

                    p=Retweet(listaInput[i].username,temp)
                    list_ret.append(p)
                    #writeFile.write(str(p.posizione) + "," + str(p.retweet) + '\n')
            except tweepy.TweepError:
                print('exception raised, waiting 15 minutes')
                print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
                print('Scrivo pickle')
                with open('./pickle/retweet_data.pkl', 'wb') as output:
                    pickle.dump(list_ret, output, pickle.HIGHEST_PROTOCOL)
                print('scrivo prima dello sleep')

                list_ret = []
                print("clear"+str(len(list_ret)))
                time.sleep(15 * 60)
            break

    return getRetweet(api,listaInput,lenLista,pos,list_ret)



def main() :
    api = connectApi.loginApi()

    with open('/home/alessandro/PycharmProjects/Tesi/TweetOldSerialization/pickle/tweetRegionali Sicilia_2017-11-01_2017-11-05_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)
        print len(retweetList)
        for i in range(0,len(retweetList)):
            print(retweetList[i].username,retweetList[i].numRetweet)
    with open('/home/alessandro/PycharmProjects/Tesi/TweetOldSerialization/pickle/tweetRegionali Sicilia_2017-11-01_2017-11-05_dictionaryReTweet.pkl', 'rb') as handler:
        Tweet = pickle.load(handler)
    for x in Tweet:
        print (Tweet[x])

    with open('/home/alessandro/PycharmProjects/Tesi/TweetOldSerialization/pickle/tweetRegionali Sicilia_2017-11-01_2017-11-05_dictionaryTweet.pkl', 'rb') as handler:
        Tweet = pickle.load(handler)
    for x in Tweet:
        print (Tweet[x])

if __name__ == '__main__':
    main()

