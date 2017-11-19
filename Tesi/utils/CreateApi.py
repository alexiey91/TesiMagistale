import tweepy
import json


def loginApi():
    path = '/home/alessandro/PycharmProjects/Tesi/'

    with open(path + 'utils/credential.json') as json_data:
        d = json.load(json_data)
        auth = tweepy.OAuthHandler(d["consumer_key"], d["consumer_secret"])
        auth.set_access_token(d["access_token"], d["access_secret"])
        api = tweepy.API(auth)
        return api
