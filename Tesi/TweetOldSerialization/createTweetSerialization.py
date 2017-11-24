import sys
import os

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got
import tweepy
import time
import datetime as dt
import pickle
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


class Retweet(object):
    user = ''
    retweet = []

    def __init__(self, user, retweet):
        self.user = user
        self.retweet = retweet


def getRetweetRicorsiva(api, listaInput, lenLista, pos, list_ret):
    if (pos == lenLista):
        return list_ret
    else:

        for i in range(pos, lenLista):
            try:
                if listaInput[i].numRetweet == 0:
                    pos = pos + 1
                    ret = Retweet(listaInput[i].username, '')
                    list_ret.append(ret)

                    print("pos=" + str(pos))

                else:
                    results = api.retweets(listaInput[i].tweetId)
                    pos = pos + 1
                    temp = []
                    for tweet in results:
                        temp.append(tweet.user.id)
                        print ("id=", tweet.user.id, " pos=", str(pos))

                    p = Retweet(listaInput[i].username, temp)
                    list_ret.append(p)
            except tweepy.TweepError:
                print('exception raised, waiting 15 minutes')
                print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
                # print('Scrivo pickle')
                # pickle.dump(list_ret, output, pickle.HIGHEST_PROTOCOL)
                # print('scrivo prima dello sleep')

                # list_ret = []
                print("check list len" + str(len(list_ret)))
                time.sleep(15 * 60)
            break

    return getRetweetRicorsiva(api, listaInput, lenLista, pos, list_ret)


def getRetweet(api, listaInput,lenLista,list_ret):


        for i in range(0, lenLista):
            try:
                if listaInput[i].numRetweet == 0:
                    ret = Retweet(listaInput[i].username, '')
                    list_ret.append(ret)

                    print("pos=" + str(i))

                else:
                    results = api.retweets(listaInput[i].tweetId)
                    temp = []
                    for tweet in results:
                        temp.append(tweet.user.id)

                    p = Retweet(listaInput[i].username, temp)
                    list_ret.append(p)
            except tweepy.TweepError:
                print('exception raised, waiting 15 minutes')
                print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
                print("check list len" + str(len(list_ret)))

                #list_ret=[]
                print("check list len dopo scrittura file" + str(len(list_ret)))
                time.sleep(15 * 60)
        return list_ret



def retweetmain(readList,query,start,stop):
    

    api = connectApi.loginApi()
    list_ret = []
    #with open('./pickle/retweet_data.pkl', 'wb') as output:
    result=getRetweet(api, readList, len(readList),list_ret)
    with open('./pickle/retweet'+query+'_'+start+'_'+stop+'_data.pkl', 'wb') as output:
        pickle.dump(result, output, pickle.HIGHEST_PROTOCOL)
    #getRetweet(api,readList,len(readList),list_ret,query,start,stop);
    print('finito getRetweet')
    with open('./pickle/retweet'+query+'_'+start+'_'+stop+'_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)
        for i in range(0, len(retweetList)):
            print (retweetList[i].user)


def main():
    # Example 1 - Get tweets by username
    # tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
    # tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

    # printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)

    # Example 2 - Get tweets by query search
    query='Sicilia'
    start="2017-10-01"
    stop="2017-11-20"
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(start).setUntil(
        stop)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    list = []
    # list.append(tweet)
    for t in range(len(tweet)):
        list.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                          tweet[t].hashtags, tweet[t].date, tweet[t].permalink))

    with open('./pickle/tweet'+query+'_'+start+'_'+stop+'_data.pkl', 'wb') as output:
        pickle.dump(list, output, pickle.HIGHEST_PROTOCOL)


        # with open('./pickle/tweet_data.pkl','rb') as input:
        #    readList = pickle.load(input)
        # for i in range(0,len(list)):

        # for i in range(0,len(readList)):
        # print(readList[i].text)

    with open('./pickle/tweet'+query+'_'+start+'_'+stop+'_data.pkl', 'rb') as input:
        readList = pickle.load(input)

    retweetmain(readList,query,start,stop)



if __name__ == '__main__':
    main()
