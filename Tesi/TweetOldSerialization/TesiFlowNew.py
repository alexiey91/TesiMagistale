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
import SentimentAnalysis.test as sentiment

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
    def __init__(self, username,count,date):
        self.username = username
        self.count = count
        self.date = date

    def __str__(self):
        return self.username+" "+str(self.count)+" "+str(self.date)



class countOccReTweet(object):
    def __init__(self, edge, count,date):
        self.edge = edge
        self.count = count
        self.date = date

    def __str__(self):
        return str(self.edge) + " " + str(self.count)+" "+str(self.date)

class Retweet(object):
    user = ''
    retweet = []
    date = ''

    def __init__(self, user, retweet,date):
        self.user = user
        self.retweet=retweet
        self.date = date


# OLD
# def getRetweet(api, listaInput, lenLista, list_ret,dizionario_tweet,dizionario_retweet,query,start,stop,char):
#     for i in range(0, lenLista):
#         try:
#             print("num",listaInput[i].numRetweet)
#             if listaInput[i].numRetweet == 0 or listaInput[i].numRetweet == '':
#                 print("ola")
#                 ret = Retweet(listaInput[i].username, '',listaInput[i].date)
#                 list_ret.append(ret)
#                 if listaInput[i].username == "marisaLaDestra":
#                     print("MARISA NELL'if")
#                 print("pos=" + str(i))
#
#             else:
#                 results = api.retweets(listaInput[i].tweetId)
#                 temp = []
#                 i=0
#                 if listaInput[i].username == "marisaLaDestra":
#                     print("MARISA NELL'else")
#                 for tweet in results:
#                     if listaInput[i].username == "marisaLaDestra":
#                         print("MARISA NELL'else")
#                     temp.append(tweet.user.screen_name)
#                     print("tweet",i,tweet.user.screen_name,listaInput[i].username)
#                     if not dizionario_retweet.has_key((tweet.user.screen_name,listaInput[i].username)):
#                            dizionario_retweet[(tweet.user.screen_name,listaInput[i].username)] = (countOccReTweet((tweet.user.screen_name,listaInput[i].username),
#                                                                                                                1/dizionario_tweet[listaInput[i].username].count,listaInput[i].date))
#                            i = i+1
#
#                     else:
#                         Numeratore = (dizionario_retweet[(tweet.user.screen_name,listaInput[i].username)].count/dizionario_tweet[listaInput[i].username].count)+1
#                         dizionario_retweet[(tweet.user.screen_name,listaInput[i].username)].count = Numeratore/dizionario_tweet[listaInput[i].username].count
#                         #print (str(dizionario_tweet[listaInput[i].username].count))
#                         i=i+1
#
#                 p = Retweet(listaInput[i].username, temp,listaInput[i].date)
#                 list_ret.append(p)
#         except tweepy.TweepError:
#             print('exception raised, waiting 15 minutes')
#             print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
#             print("check list len" + str(len(list_ret)))
#             print("check list len dopo scrittura file" + str(len(list_ret)))
#             time.sleep(15 * 60)
#
#     print('scrivo su pickle il dizionario ottenuto'+char)
#     with open('./pickle/RegionaliSiciliaTest/tweet' + query + '_' + start + '_' + stop + '_dictionaryReTweet'+char+'.pkl', 'wb') as output:
#         pickle.dump(dizionario_retweet,output, pickle.HIGHEST_PROTOCOL)
#     print ('fatto')
#     return list_ret


def getRetweet(api, listaInput, lenLista, list_ret,dizionario_tweet,dizionario_retweet,query,start,stop,char):
    for i in listaInput:
        try:
            #print("num",i.numRetweet)
            if i.numRetweet == 0 or i.numRetweet == '':

                ret = Retweet(i.username, '',i.date)
                list_ret.append(ret)

                print("pos=", i)

            else:
                results = api.retweets(i.tweetId)
                temp = []
                k=0

                for tweet in results:

                    print("tweet",k,tweet.user.screen_name,i.username)
                    if not dizionario_retweet.has_key((tweet.user.screen_name,i.username)):
                           # dizionario_retweet[(tweet.user.screen_name,i.username)] = (countOccReTweet((tweet.user.screen_name,i.username),
                           #                                                                                     1/dizionario_tweet[i.username].count,i.date))
                           dizionario_retweet[(tweet.user.screen_name,i.username)] = (countOccReTweet((tweet.user.screen_name,i.username),1,i.date))
                           temp.append(tweet.user.screen_name)
                           k = k+1

                    else:
                        #Numeratore = (dizionario_retweet[(tweet.user.screen_name,i.username)].count/dizionario_tweet[i.username].count)+1
                        dizionario_retweet[(tweet.user.screen_name,i.username)].count = dizionario_retweet[(tweet.user.screen_name,i.username)].count+1
                        #print (str(dizionario_tweet[listaInput[i].username].count))
                        temp.append(tweet.user.screen_name)
                        k=k+1

                p = Retweet(i.username,temp,i.date)
                temp=[]
                list_ret.append(p)
        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
            print("check list len" + str(len(list_ret)))
            print("check list len dopo scrittura file" + str(len(list_ret)))
            time.sleep(15 * 60)

    print('scrivo su pickle il dizionario ottenuto'+char)
    with open('./pickle/'+query+'TestAWS/Novembre/tweet' + query + '_' + start + '_' + stop + '_dictionaryReTweet'+char+'.pkl', 'wb') as output:
        pickle.dump(dizionario_retweet,output, pickle.HIGHEST_PROTOCOL)
    print ('fatto')
    return list_ret



def retweetmain(readList, query, start, stop,dizionario_tweet,char):
    api = connectApi.loginApi()
    list_ret = []
    dizionario_retweet = {}
    # with open('./pickle/retweet_data.pkl', 'wb') as output:
    result = getRetweet(api, readList, len(readList), list_ret,dizionario_tweet,dizionario_retweet,query,start,stop,char)
    with open('./pickle/'+query+'TestAWS/Novembre/retweet'+char+ query + '_' + start + '_' + stop + '_data.pkl', 'wb') as output:
        pickle.dump(result, output, pickle.HIGHEST_PROTOCOL)
    # getRetweet(api,readList,len(readList),list_ret,query,start,stop);
    print('finito getRetweet')
    with open('./pickle/'+query+'TestAWS/Novembre/retweet'+char + query + '_' + start + '_' + stop + '_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)
        for i in range(0, len(retweetList)):
            print (retweetList[i].user)


def main():
    print "Start"
    query = '#' + sys.argv[1]
    print (query)
    start = "2017-09-01"
    stop = "2017-11-30"
    #Creo il dizionario per il filtraggio degli hashtag
    # dizionario_hashtag = {}
    # with open('../utils/ListaHashtag.txt', 'r') as fileHashtags:
    #
    #     for line in fileHashtags:
    #         if not dizionario_hashtag.has_key(line.strip()):
    #             dizionario_hashtag[line] = '#'+line.strip().lower()

    # for x in dizionario_hashtag:
    #      print(len(dizionario_hashtag))
    #      print(dizionario_hashtag[x])
    if not os.path.exists('pickle/'+query+'TestAWS/Novembre/'):
        os.makedirs('pickle/'+query+'TestAWS/Novembre/')
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(start).setUntil(
        stop)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    list = []
    listRed = []
    listBlue = []
    listYellow = []
    #creo il dizionario con l'oggetto tweetOcc
    dizionario_tweet = {}
    dizionario_tweet_Blue = {}
    dizionario_tweet_Red = {}
    dizionario_tweet_Yellow = {}
    #for t in range(len(tweet)):
    for t in range(len(tweet)):

        # print (tweet[t].hashtags)
        # list_hash = tweet[t].hashtags.strip().lower().split(" ")
        #
        # b3 = [val for val in list_hash if val in dizionario_hashtag.values()]
        #
        # if len(b3)==0:
        #     continue
        # else:
            list.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                                     tweet[t].hashtags, tweet[t].date, tweet[t].permalink))

            # if not dizionario_tweet.has_key(tweet[t].username):
            #     dizionario_tweet[tweet[t].username] = (countOccTweet(tweet[t].username, 1,tweet[t].date))
            #
            # else:
            #     # dizionario_tweet.update[tweet[t].username](countOccTweet(tweet[t].username,countOccTweet.count+1))
            #     dizionario_tweet[tweet[t].username].count += 1

            if(sentiment.checkPartition(u._unidecode(tweet[t].text).lower()) == "ForzaItalia"):
                listBlue.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                                     tweet[t].hashtags, tweet[t].date, tweet[t].permalink))
                if not dizionario_tweet_Blue.has_key(tweet[t].username):
                    dizionario_tweet_Blue[tweet[t].username] = (countOccTweet(tweet[t].username, 1,tweet[t].date))
                else:
                    dizionario_tweet_Blue[tweet[t].username].count+=1

            elif(sentiment.checkPartition(u._unidecode(tweet[t].text).lower()) == "5stelle"):
                listRed.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                                     tweet[t].hashtags, tweet[t].date, tweet[t].permalink))
                if not dizionario_tweet_Red.has_key(tweet[t].username):
                    dizionario_tweet_Red[tweet[t].username] = (countOccTweet(tweet[t].username, 1,tweet[t].date))
                else:
                    dizionario_tweet_Red[tweet[t].username].count += 1

            elif(sentiment.checkPartition(u._unidecode(tweet[t].text).lower()) == "Altro"):
                listYellow.append(Tweet(tweet[t].username, tweet[t].id, tweet[t].retweets, tweet[t].text, tweet[t].mentions,
                                     tweet[t].hashtags, tweet[t].date, tweet[t].permalink))
                if not dizionario_tweet_Yellow.has_key(tweet[t].username):
                 dizionario_tweet_Yellow[tweet[t].username] = (countOccTweet(tweet[t].username, 1, tweet[t].date))
                else:
                 dizionario_tweet_Yellow[tweet[t].username].count += 1





    with open('./pickle/'+query+'TestAWS/Novembre/tweetBlue' + query + '_' + start + '_' + stop + '_data.pkl', 'wb') as output:
        pickle.dump(listBlue, output, pickle.HIGHEST_PROTOCOL)

    with open('./pickle/'+query+'TestAWS/Novembre/tweetBlue' + query + '_' + start + '_' + stop + '_dictionaryTweet.pkl', 'wb') as output:
        pickle.dump(dizionario_tweet_Blue, output, pickle.HIGHEST_PROTOCOL)

    with open('./pickle/'+query+'TestAWS/Novembre/tweetRed' + query + '_' + start + '_' + stop + '_data.pkl', 'wb') as output:
            pickle.dump(listRed, output, pickle.HIGHEST_PROTOCOL)

    with open('./pickle/'+query+'TestAWS/Novembre/tweetRed' + query + '_' + start + '_' + stop + '_dictionaryTweet.pkl', 'wb') as output:
            pickle.dump(dizionario_tweet_Red, output, pickle.HIGHEST_PROTOCOL)

    with open('./pickle/'+query+'TestAWS/Novembre/tweetYellow' + query + '_' + start + '_' + stop + '_data.pkl', 'wb') as output:
            pickle.dump(listYellow, output, pickle.HIGHEST_PROTOCOL)

    with open('./pickle/'+query+'TestAWS/Novembre/tweetYellow' + query + '_' + start + '_' + stop + '_dictionaryTweet.pkl', 'wb') as output:
            pickle.dump(dizionario_tweet_Yellow, output, pickle.HIGHEST_PROTOCOL)

    # with open('./pickle/'+query+'TestAWS/tweetAll' + query + '_' + start + '_' + stop + '_data.pkl', 'wb') as output:
    #     pickle.dump(list, output, pickle.HIGHEST_PROTOCOL)
    #
    # with open('./pickle/'+query+'TestAWS/tweetAll' + query + '_' + start + '_' + stop + '_dictionaryTweet.pkl',
    #           'wb') as output:
    #     pickle.dump(dizionario_tweet, output, pickle.HIGHEST_PROTOCOL)

        #for x in dizionario_tweet:
        #     print (dizionario_tweet[x])

    # print('Dopo Scritturea PICKLE')
    # with open('./pickle/tweet' + query + '_' + start + '_' + stop + '_data.pkl', 'rb') as input:
    #     readList = pickle.load(input)
    #
    #     for i in range(0, len(readList)):
    #         print(len(readList))
    #         print(readList[i].username,readList[i].numRetweet,readList[i].text,readList[i].hashtags)

    retweetmain(listRed, query, start, stop,dizionario_tweet_Red,"Red")
    retweetmain(listBlue, query, start, stop, dizionario_tweet_Blue, "Blue")
    retweetmain(listYellow, query, start, stop, dizionario_tweet_Yellow, "Yellow")
    #retweetmain(list, query, start, stop, dizionario_tweet, "All")
    with open('./pickle/'+query+'TestAWS/Novembre/Finito'+str(dt.datetime.now()),"wb") as output:
        pickle.dump(str(dt.datetime.now),output,pickle.HIGHEST_PROTOCOL)
    print "Finish"
if __name__ == '__main__':
    main()
