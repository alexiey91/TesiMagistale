from __future__ import division
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

    def __init__(self, user, retweet):
        self.user = user
        self.retweet = retweet



def getRetweet(api, listaInput, lenLista, list_ret,dizionario_tweet,dizionario_retweet,query,start,stop):
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

                    if not dizionario_retweet.has_key((tweet.user.screen_name,listaInput[i].username)):
                           dizionario_retweet[(tweet.user.screen_name,listaInput[i].username)] = (countOccReTweet((tweet.user.screen_name,listaInput[i].username),
                                                                                                               1/dizionario_tweet[listaInput[i].username].count))

                    else:
                        Numeratore = (dizionario_retweet[(tweet.user.screen_name,listaInput[i].username)].count/dizionario_tweet[listaInput[i].username].count)+1
                        dizionario_retweet[(tweet.user.screen_name,listaInput[i].username)].count = Numeratore/dizionario_tweet[listaInput[i].username].count
                        #print (str(dizionario_tweet[listaInput[i].username].count))

                p = Retweet(listaInput[i].username, temp)
                list_ret.append(p)
        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
            print("check list len" + str(len(list_ret)))
            print("check list len dopo scrittura file" + str(len(list_ret)))
            time.sleep(15 * 60)

    print('scrivo su pickle il dizionario ottenuto')
    with open('./pickle/tweet' + query + '_' + start + '_' + stop + '_dictionaryReTweet.pkl', 'wb') as output:
        pickle.dump(dizionario_retweet,output, pickle.HIGHEST_PROTOCOL)
    print ('fatto')
    return list_ret


def retweetmain(readList, query, start, stop,dizionario_tweet):
    api = connectApi.loginApi()
    list_ret = []
    dizionario_retweet = {}
    # with open('./pickle/retweet_data.pkl', 'wb') as output:
    result = getRetweet(api, readList, len(readList), list_ret,dizionario_tweet,dizionario_retweet,query,start,stop)
    with open('./pickle/retweet' + query + '_' + start + '_' + stop + '_data.pkl', 'wb') as output:
        pickle.dump(result, output, pickle.HIGHEST_PROTOCOL)
    # getRetweet(api,readList,len(readList),list_ret,query,start,stop);
    print('finito getRetweet')
    with open('./pickle/retweet' + query + '_' + start + '_' + stop + '_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)
        for i in range(0, len(retweetList)):
            print (retweetList[i].user)


def main():
    # Example 1 - Get tweets by username
    # tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
    # tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

    # printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)

    # Example 2 - Get tweets by query search
    query = 'Regionali Sicilia'
    start = "2017-10-01"
    stop = "2017-11-20"
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(start).setUntil(
        stop)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    list = []
    #creo il dizionario con l'oggetto tweetOcc
    dizionario_tweet = {}
    # list.append(tweet)
    #for t in range(len(tweet)):
    for t in range(len(tweet)):
        print (tweet[t].username,str(tweet[t].retweets), tweet[t].text,str(tweet[t].date))
        list.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                          tweet[t].hashtags, tweet[t].date, tweet[t].permalink))
        if not dizionario_tweet.has_key(tweet[t].username):
                dizionario_tweet[tweet[t].username] = (countOccTweet(tweet[t].username,1))

        else:
             # dizionario_tweet.update[tweet[t].username](countOccTweet(tweet[t].username,countOccTweet.count+1))
             dizionario_tweet[tweet[t].username].count += 1
    with open('./pickle/tweet' + query + '_' + start + '_' + stop + '_data.pkl', 'wb') as output:
        pickle.dump(list, output, pickle.HIGHEST_PROTOCOL)

    with open('./pickle/tweet' + query + '_' + start + '_' + stop + '_dictionaryTweet.pkl', 'wb') as output:
        pickle.dump(dizionario_tweet, output, pickle.HIGHEST_PROTOCOL)

        #for x in dizionario_tweet:
        #     print (dizionario_tweet[x])


    with open('./pickle/tweet' + query + '_' + start + '_' + stop + '_data.pkl', 'rb') as input:
        readList = pickle.load(input)



    retweetmain(readList, query, start, stop,dizionario_tweet)


if __name__ == '__main__':
    main()
