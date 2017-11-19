import sys

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got
import tweepy
import time
import datetime as dt
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils.CreateApi as connectApi


def printTweet(descr, t):
    print(descr)
    print ("ID: %s" % t.id)
    print("Username: %s" % t.username)
    print("Retweets: %d" % t.retweets)
    print("Text: %s" % t.text)
    print("Mentions: %s" % t.mentions)
    print("Hashtags: %s\n" % t.hashtags)
    print("Date: %s\n" % t.date)
    print("Permaling: %s\n" % t.permalink)

def retriveRetweetId(t):
    api = connectApi.loginApi()

    results = api.retweets(t.id)
    list=[]
    for tweet in results:
            # retweets = t.GetRetweets(tweet.GetId())
            # users = [retweet.GetUser().GetScreenName() for retweet in retweets]
            list.append(tweet.user.id)

            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
            time.sleep(15 * 60)


    return list


def createLine(t):

    if "," not in t.text:
        linea = t.username +","+ str(t.id) +","+str(t.retweets)+","+t.text.encode('utf-8')+","+ t.mentions.encode('utf-8') +","+ t.hashtags.encode('utf-8') +","+str(t.date) + ","+str(t.permalink)+"\n"
    else:
        linea = t.username +","+ str(t.id) + ","+str(t.retweets)+","+t.text.replace(",","").encode('utf-8')+","+ t.mentions.encode('utf-8') +","+ t.hashtags.encode('utf-8') +","+str(t.date) + ","+str(t.permalink)+"\n"


    return linea


def main():



    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('Regionali Sicilia').setSince("2017-11-01").setUntil(
        "2017-11-05")
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    list = []
    list.append(tweet)
    # print("lista",list)
    num_tweet = len(tweet)
    csv = open('RegionaliSicilia.csv', 'w+')
    indice =0
    for t in range(len(tweet)):
        try:
            printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet[t])
            l=createLine(tweet[t])
            csv.write(str(l))
            indice = indice +1
        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
            time.sleep(15 * 60)
            continue



if __name__ == '__main__':
    main()
