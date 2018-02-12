from __future__ import division
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import got
import tweepy
import time
import datetime as dt
import pickle
import unidecode as u

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils.CreateApi as connectApi

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import SentimentAnalysis.sentiment as sentiment


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
    def __init__(self, username, count, date):
        self.username = username
        self.count = count
        self.date = date

    def __str__(self):
        return self.username + " " + str(self.count) + " " + str(self.date)


class countOccReTweet(object):
    def __init__(self, edge, count, date):
        self.edge = edge
        self.count = count
        self.date = date

    def __str__(self):
        return str(self.edge) + " " + str(self.count) + " " + str(self.date)


class Retweet(object):
    user = ''
    retweet = []
    date = ''

    def __init__(self, user, retweet, date):
        self.user = user
        self.retweet = retweet
        self.date = date


'''
@param api: the credential to access to Twitter service
@param listaInput: the list of tweet
@param list_ret: list of retweet 
@param dizionario_retweet: dictionary use to save all retweet for the selected tweet
@param query: hashtag searched
@param start: starting time of research
@param stop: stopping time of research
@return the list of retweet object
'''


def getRetweet(api, listaInput, lenLista, list_ret, dizionario_tweet, dizionario_retweet, query, start, stop, char):
    for i in listaInput:
        try:
            # print("num",i.numRetweet)
            if i.numRetweet == 0 or i.numRetweet == '':

                ret = Retweet(i.username, '', i.date)
                list_ret.append(ret)

                print("pos=", i)

            else:
                results = api.retweets(i.tweetId)
                temp = []
                k = 0

                for tweet in results:

                    print("tweet", k, tweet.user.screen_name, i.username)
                    if not dizionario_retweet.has_key((tweet.user.screen_name, i.username)):
                        # dizionario_retweet[(tweet.user.screen_name,i.username)] = (countOccReTweet((tweet.user.screen_name,i.username),
                        #                                                                                     1/dizionario_tweet[i.username].count,i.date))
                        dizionario_retweet[(tweet.user.screen_name, i.username)] = (
                        countOccReTweet((tweet.user.screen_name, i.username), 1, i.date))
                        temp.append(tweet.user.screen_name)
                        k = k + 1

                    else:
                        # Numeratore = (dizionario_retweet[(tweet.user.screen_name,i.username)].count/dizionario_tweet[i.username].count)+1
                        dizionario_retweet[(tweet.user.screen_name, i.username)].count = dizionario_retweet[(
                        tweet.user.screen_name, i.username)].count + 1
                        # print (str(dizionario_tweet[listaInput[i].username].count))
                        temp.append(tweet.user.screen_name)
                        k = k + 1

                p = Retweet(i.username, temp, i.date)
                temp = []
                list_ret.append(p)
        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
            print("check list len" + str(len(list_ret)))
            print("check list len dopo scrittura file" + str(len(list_ret)))
            time.sleep(15 * 60)

    print('scrivo su pickle il dizionario ottenuto' + char)
    with open(
            './pickle/' + query + 'TestAWS/Dicembre/tweet' + query + '_' + start + '_' + stop + '_dictionaryReTweet' + char + '.pkl',
            'wb') as output:
        pickle.dump(dizionario_retweet, output, pickle.HIGHEST_PROTOCOL)
    print ('fatto')
    return list_ret


def retweetmain(readList, query, start, stop, dizionario_tweet, char):
    api = connectApi.loginApi()
    list_ret = []
    dizionario_retweet = {}
    # with open('./pickle/retweet_data.pkl', 'wb') as output:
    result = getRetweet(api, readList, len(readList), list_ret, dizionario_tweet, dizionario_retweet, query, start,
                        stop, char)

    with open('./pickle/' + query + 'TestAWS/Dicembre/retweet' + char + query + '_' + start + '_' + stop + '_data.pkl',
              'wb') as output:
        pickle.dump(result, output, pickle.HIGHEST_PROTOCOL)
    # getRetweet(api,readList,len(readList),list_ret,query,start,stop);
    print('finito getRetweet')
    with open('./pickle/' + query + 'TestAWS/Dicembre/retweet' + char + query + '_' + start + '_' + stop + '_data.pkl',
              'rb') as input:
        retweetList = pickle.load(input)
        for i in range(0, len(retweetList)):
            print (retweetList[i].user)


def main():
    print "Start"
    query = '#' + sys.argv[1]
    print (query)
    start = "2017-09-01"
    stop = "2017-12-20"

    if not os.path.exists('pickle/' + query + 'TestAWS/Dicembre/'):
        os.makedirs('pickle/' + query + 'TestAWS/Dicembre/')
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(start).setUntil(
        stop)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    list = []
    listRed = []
    listBlue = []
    listYellow = []
    # creo il dizionario con l'oggetto tweetOcc
    dizionario_tweet = {}
    dizionario_tweet_Blue = {}
    dizionario_tweet_Red = {}
    dizionario_tweet_Yellow = {}
    # for t in range(len(tweet)):
    for t in range(len(tweet)):


        list.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                          tweet[t].hashtags, tweet[t].date, tweet[t].permalink))



        if (sentiment.checkPartition(u._unidecode(tweet[t].text).lower()) == "Red"):
            listBlue.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                                  tweet[t].hashtags, tweet[t].date, tweet[t].permalink))
            if not dizionario_tweet_Blue.has_key(tweet[t].username):
                dizionario_tweet_Blue[tweet[t].username] = (countOccTweet(tweet[t].username, 1, tweet[t].date))
            else:
                dizionario_tweet_Blue[tweet[t].username].count += 1

        elif (sentiment.checkPartition(u._unidecode(tweet[t].text).lower()) == "Blue"):
            listRed.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                                 tweet[t].hashtags, tweet[t].date, tweet[t].permalink))
            if not dizionario_tweet_Red.has_key(tweet[t].username):
                dizionario_tweet_Red[tweet[t].username] = (countOccTweet(tweet[t].username, 1, tweet[t].date))
            else:
                dizionario_tweet_Red[tweet[t].username].count += 1



    with open('./pickle/' + query + 'TestAWS/Dicembre/tweetBlue' + query + '_' + start + '_' + stop + '_data.pkl',
              'wb') as output:
        pickle.dump(listBlue, output, pickle.HIGHEST_PROTOCOL)

    with open(
            './pickle/' + query + 'TestAWS/Dicembre/tweetBlue' + query + '_' + start + '_' + stop + '_dictionaryTweet.pkl',
            'wb') as output:
        pickle.dump(dizionario_tweet_Blue, output, pickle.HIGHEST_PROTOCOL)

    with open('./pickle/' + query + 'TestAWS/Dicembre/tweetRed' + query + '_' + start + '_' + stop + '_data.pkl',
              'wb') as output:
        pickle.dump(listRed, output, pickle.HIGHEST_PROTOCOL)

    with open(
            './pickle/' + query + 'TestAWS/Dicembre/tweetRed' + query + '_' + start + '_' + stop + '_dictionaryTweet.pkl',
            'wb') as output:
        pickle.dump(dizionario_tweet_Red, output, pickle.HIGHEST_PROTOCOL)

    with open('./pickle/' + query + 'TestAWS/Dicembre/tweetYellow' + query + '_' + start + '_' + stop + '_data.pkl',
              'wb') as output:
        pickle.dump(listYellow, output, pickle.HIGHEST_PROTOCOL)

    with open(
            './pickle/' + query + 'TestAWS/Dicembre/tweetYellow' + query + '_' + start + '_' + stop + '_dictionaryTweet.pkl',
            'wb') as output:
        pickle.dump(dizionario_tweet_Yellow, output, pickle.HIGHEST_PROTOCOL)


    retweetmain(listRed, query, start, stop, dizionario_tweet_Red, "Red")
    retweetmain(listBlue, query, start, stop, dizionario_tweet_Blue, "Blue")
    retweetmain(listYellow, query, start, stop, dizionario_tweet_Yellow, "Yellow")
    # retweetmain(list, query, start, stop, dizionario_tweet, "All")
    with open('./pickle/' + query + 'TestAWS/Dicembre/Finito' + str(dt.datetime.now()), "wb") as output:
        pickle.dump(str(dt.datetime.now), output, pickle.HIGHEST_PROTOCOL)
    print "Finish"


if __name__ == '__main__':
    main()
