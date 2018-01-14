from __future__ import division
import pickle
import os
from dateutil import parser
import datetime
import networkx as nx
import matplotlib.pyplot as plt
import community
import numpy as np
import operator
import heapq
import math


nodi_isolati = []

class Retweet(object):
    user = ''
    retweet = []
    text=''
    date = ''

    def __init__(self, user, retweet,date):
        self.user = user
        self.retweet = retweet
        self.date = date


class countOccReTweet(object):
    edge=''
    count=0
    date=''
    def __init__(self, edge, count,date):
        self.edge = edge
        self.count = count
        self.date = date

    def __str__(self):
        return str(self.edge) + " " + str(self.count)+" "+str(self.date)

class countWeighEdge(object):
    node = ''
    count = 0


    def __init__(self, node, count):
        self.node = node
        self.count = count

    def __str__(self):
        return str(self.node) + " " + str(self.count)


def release_list(a):
   del a[:]
   del a

def deleteList(List1,List2):
    for i in List1:
        for j in List2:

            if i.user == j.user:
                 List2.remove(j)

def mergeListPartitionNoDate(hashtag,color):

    with open('../TweetOldSerialization/pickle/#'+hashtag[0]+'TestAWS/retweet'+color+'#'+hashtag[0]+'_2017-09-01_2017-12-20_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)


    with open('../TweetOldSerialization/pickle/#errorTestAWS/retweet'+color+'.pkl','rb') as input:
        retweetList2 = pickle.load(input)
    for i in retweetList2:
        retweetList.append(i)
    release_list(retweetList2)



    with open('../TweetOldSerialization/pickle/#'+hashtag[2]+'TestAWS/retweet' + color + '#'+hashtag[2]+'_2017-09-01_2017-12-20_data.pkl','rb') as input:
        retweetList3 = pickle.load(input)
    for i in retweetList3:
        retweetList.append(i)
    release_list(retweetList3)
    with open('../TweetOldSerialization/pickle/#'+hashtag[3]+'TestAWS/retweet' + color + '#'+hashtag[3]+'_2017-09-01_2017-12-20_data.pkl',
            'rb') as input:
        retweetList4 = pickle.load(input)
    for i in retweetList4:
        retweetList.append(i)
    release_list(retweetList4)

    with open('../TweetOldSerialization/pickle/#' + hashtag[4] + 'TestAWS/retweet' + color + '#' + hashtag[4] + '_2017-09-01_2017-12-20_data.pkl',
              'rb') as input:
        retweetList5 = pickle.load(input)
    for i in retweetList5:
        retweetList.append(i)
    release_list(retweetList5)

    return retweetList

def mergeListPartition(hashtag,color,date):
    list=[]
    with open('../TweetOldSerialization/pickle/#'+hashtag[0]+'TestAWS/retweet'+color+'#'+hashtag[0]+'_2017-09-01_2017-12-20_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)
    for i in retweetList:
        t = str(i.date.strftime('%Y-%m-%d'))

        if parser.parse(t) <= parser.parse(date):
            list.append(i)
        else:
            continue
        #retweetList.append(i)

    with open('../TweetOldSerialization/pickle/#errorTestAWS/retweet'+color+'.pkl','rb') as input:
        retweetList2 = pickle.load(input)
    for i in retweetList2:
        t = str(i.date.strftime('%Y-%m-%d'))

        if parser.parse(t) <= parser.parse(date):
            list.append(i)
        else:
            continue
    release_list(retweetList2)



    with open('../TweetOldSerialization/pickle/#'+hashtag[2]+'TestAWS/retweet' + color + '#'+hashtag[2]+'_2017-09-01_2017-12-20_data.pkl','rb') as input:
        retweetList3 = pickle.load(input)
    for i in retweetList3:
        t = str(i.date.strftime('%Y-%m-%d'))

        if parser.parse(t) <= parser.parse(date):
            list.append(i)
        else:
            continue
    release_list(retweetList3)
    with open('../TweetOldSerialization/pickle/#'+hashtag[3]+'TestAWS/retweet' + color + '#'+hashtag[3]+'_2017-09-01_2017-12-20_data.pkl',
            'rb') as input:
        retweetList4 = pickle.load(input)
    for i in retweetList4:
        t = str(i.date.strftime('%Y-%m-%d'))

        if parser.parse(t) <= parser.parse(date):
            list.append(i)
        else:
            continue
    release_list(retweetList4)

    with open('../TweetOldSerialization/pickle/#' + hashtag[4] + 'TestAWS/retweet' + color + '#' + hashtag[4] + '_2017-09-01_2017-12-20_data.pkl',
              'rb') as input:
        retweetList5 = pickle.load(input)
    for i in retweetList5:
        t = str(i.date.strftime('%Y-%m-%d'))

        if parser.parse(t) <= parser.parse(date):
            list.append(i)
        else:
            continue
    release_list(retweetList5)

    return list


def mergeProbDicPartition(hashtag,color,date):
    probFull={}
    with open ('../TweetOldSerialization/pickle/#'+hashtag[0]+'TestAWS/tweet#'+hashtag[0]+'_2017-09-01_2017-12-20_dictionaryReTweet'+color+'.pkl', 'rb') as input:
        probRetBlue = pickle.load(input)
    for i in  probRetBlue:
        print i
        t = str(probRetBlue[i].date.strftime('%Y-%m-%d'))
        if not probFull.has_key(probRetBlue[i].edge) and parser.parse(t) <= parser.parse(date):
            probFull[probRetBlue[i].edge]= probRetBlue[i].count
        else:
            continue
    with open ('../TweetOldSerialization/pickle/#errorTestAWS/dictionaryReTweet'+color+'.pkl', 'rb') as input:
        probRetBlue2 = pickle.load(input)
        for i in probRetBlue2:
            t = str(probRetBlue2[i].date.strftime('%Y-%m-%d'))
            if not probFull.has_key(probRetBlue2[i].edge) and parser.parse(t) <= parser.parse(date):
                probFull[probRetBlue2[i].edge] = probRetBlue2[i].count
            else:
                continue
    with open ('../TweetOldSerialization/pickle/#'+hashtag[2]+'TestAWS/tweet#'+hashtag[2]+'_2017-09-01_2017-12-20_dictionaryReTweet'+color+'.pkl', 'rb') as input:
        probRetBlue3 = pickle.load(input)
        for i in probRetBlue3:
            t = str(probRetBlue3[i].date.strftime('%Y-%m-%d'))
            if not probFull.has_key(probRetBlue3[i].edge) and parser.parse(t) <= parser.parse(date):
                probFull[probRetBlue3[i].edge] = probRetBlue3[i].count
            else:
                continue
    with open ('../TweetOldSerialization/pickle/#'+hashtag[3]+'TestAWS/tweet#'+hashtag[3]+'_2017-09-01_2017-12-20_dictionaryReTweet'+color+'.pkl', 'rb') as input:
        probRetBlue4 = pickle.load(input)
        for i in probRetBlue4:
            t = str(probRetBlue4[i].date.strftime('%Y-%m-%d'))

            if not probFull.has_key(probRetBlue4[i].edge) and parser.parse(t) <= parser.parse(date):
                probFull[probRetBlue4[i].edge] = probRetBlue4[i].count
            else:
                continue

    with open ('../TweetOldSerialization/pickle/#'+hashtag[4]+'TestAWS/tweet#'+hashtag[4]+'_2017-09-01_2017-12-20_dictionaryReTweet'+color+'.pkl', 'rb') as input:
        probRetBlue5 = pickle.load(input)
        for i in probRetBlue5:
            t = str(probRetBlue5[i].date.strftime('%Y-%m-%d'))

            if not probFull.has_key(probRetBlue5[i].edge) and  parser.parse(t) <= parser.parse(date):
                probFull[probRetBlue5[i].edge] = probRetBlue5[i].count
            else:
                continue

    return probFull


def mergeProbDicPartitionNoDate(hashtag, color):
    probFull = {}
    with open('../TweetOldSerialization/pickle/#' + hashtag[0] + 'TestAWS/tweet#' + hashtag[
        0] + '_2017-09-01_2017-12-20_dictionaryReTweet' + color + '.pkl', 'rb') as input:
        probRetBlue = pickle.load(input)
    for i in probRetBlue:

        if not probFull.has_key(probRetBlue[i].edge):
            probFull[probRetBlue[i].edge] = probRetBlue[i].count
        else:
            continue
    with open('../TweetOldSerialization/pickle/#errorTestAWS/dictionaryReTweet' + color + '.pkl', 'rb') as input:
        probRetBlue2 = pickle.load(input)
        for i in probRetBlue2:
            if not probFull.has_key(probRetBlue2[i].edge):
                probFull[probRetBlue2[i].edge] = probRetBlue2[i].count
            else:
                continue
    with open('../TweetOldSerialization/pickle/#' + hashtag[2] + 'TestAWS/tweet#' + hashtag[
        2] + '_2017-09-01_2017-12-20_dictionaryReTweet' + color + '.pkl', 'rb') as input:
        probRetBlue3 = pickle.load(input)
        for i in probRetBlue3:
            if not probFull.has_key(probRetBlue3[i].edge):
                probFull[probRetBlue3[i].edge] = probRetBlue3[i].count
            else:
                continue
    with open('../TweetOldSerialization/pickle/#' + hashtag[3] + 'TestAWS/tweet#' + hashtag[
        3] + '_2017-09-01_2017-12-20_dictionaryReTweet' + color + '.pkl', 'rb') as input:
        probRetBlue4 = pickle.load(input)
        for i in probRetBlue4:
            if not probFull.has_key(probRetBlue4[i].edge):
                probFull[probRetBlue4[i].edge] = probRetBlue4[i].count
            else:
                continue

    with open('../TweetOldSerialization/pickle/#' + hashtag[4] + 'TestAWS/tweet#' + hashtag[
        4] + '_2017-09-01_2017-12-20_dictionaryReTweet' + color + '.pkl', 'rb') as input:
        probRetBlue5 = pickle.load(input)
        for i in probRetBlue5:
            if not probFull.has_key(probRetBlue5[i].edge):
                probFull[probRetBlue5[i].edge] = probRetBlue5[i].count
            else:
                continue

    return probFull


def main():
    print()
    hashtags = ['EleSicilia', 'elezionisicilia2017', 'elezionisicilia', 'regionalisicilia2017', 'regionalisicilia']
    colors = ['Blue','Red','Yellow']

    retweetListAllBlue = mergeListPartitionNoDate(hashtags,colors[0])
    print len (retweetListAllBlue)

    for i in retweetListAllBlue:

        print(i.user)



    if not os.path.exists('./pickle/ElezioniSiciliaGraph/retweetListBlue.pkl'):
        os.makedirs('pickle/ElezioniSiciliaGraph/')

    with open('./pickle/ElezioniSiciliaGraph/retweetListBlue.pkl', 'wb') as output:
            pickle.dump(retweetListAllBlue, output, pickle.HIGHEST_PROTOCOL)

    retweetListAllRed = mergeListPartitionNoDate(hashtags,colors[1])

    deleteList(retweetListAllBlue,retweetListAllRed)

    with open('./pickle/ElezioniSiciliaGraph/retweetListRed.pkl', 'wb') as output:
        pickle.dump(retweetListAllRed, output, pickle.HIGHEST_PROTOCOL)

    retweetListAllYellow = mergeListPartitionNoDate(hashtags, colors[2])

    deleteList(retweetListAllBlue, retweetListAllYellow)

    with open('./pickle/ElezioniSiciliaGraph/retweetListYellow.pkl', 'wb') as output:
        pickle.dump(retweetListAllYellow, output, pickle.HIGHEST_PROTOCOL)


    probRetBlue=mergeProbDicPartitionNoDate(hashtags,colors[0])

    with open('./pickle/ElezioniSiciliaGraph/probRetBlue.pkl', 'wb') as output:
        pickle.dump(probRetBlue, output, pickle.HIGHEST_PROTOCOL)

    probRetRed = mergeProbDicPartitionNoDate(hashtags, colors[1])

    with open('./pickle/ElezioniSiciliaGraph/probRetRed.pkl', 'wb') as output:
        pickle.dump(probRetRed, output, pickle.HIGHEST_PROTOCOL)

    probRetYellow = mergeProbDicPartitionNoDate(hashtags, colors[2])

    with open('./pickle/ElezioniSiciliaGraph/probRetYellow.pkl', 'wb') as output:
        pickle.dump(probRetYellow, output, pickle.HIGHEST_PROTOCOL)



if __name__ == '__main__':
    main()