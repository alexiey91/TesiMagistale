from __future__ import division
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import community
import numpy as np
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

def createGraph(retweetList,probDiz):
    G = nx.DiGraph()
    #print(retweetList[1][1])
    for i in range(0,len(retweetList)):
       # print ("pos" + str(i)+"username="+ retweetList[i].user +"ret="+str(retweetList[i].retweet))
        if(  len(retweetList[i].retweet)==0 or  retweetList[i].retweet == None ):
            G.add_node(retweetList[i].user,color='green')

        else:
            for j in range(0,len(retweetList[i].retweet)):
                # print(retweetList[i].retweet[j],retweetList[i].user)
                 if probDiz.has_key((retweetList[i].retweet[j],retweetList[i].user)):
                    G.add_edge(retweetList[i].retweet[j],retweetList[i].user,weight=probDiz.get((retweetList[i].retweet[j],retweetList[i].user)))
                 else:
                     G.add_edge(retweetList[i].retweet[j],retweetList[i].user)

    return G




def createUndirectGraph(retweetList):
    G = nx.Graph()
    #print(retweetList[1][1])
    for i in range(0,len(retweetList)):
       # print ("pos" + str(i)+"username="+ retweetList[i].user +"ret="+str(retweetList[i].retweet))
        if(  len(retweetList[i].retweet)==0 or  retweetList[i].retweet == None ):
            G.add_node(retweetList[i].user,color='green')

        else:
            for j in range(0,len(retweetList[i].retweet)):
                 # print(retweetList[i].retweet[j],retweetList[i].user)
                 # if probDiz.has_key((retweetList[i].retweet[j],retweetList[i].user)):
                 #    G.add_edge(retweetList[i].retweet[j],retweetList[i].user,weight=probDiz.get((retweetList[i].retweet[j],retweetList[i].user)))
                 # else:
                     G.add_edge(retweetList[i].retweet[j],retweetList[i].user)

    return G


def createDirectNoWeightGraph(retweetList):
    G = nx.DiGraph()
    #print(retweetList[1][1])
    for i in range(0,len(retweetList)):
       # print ("pos" + str(i)+"username="+ retweetList[i].user +"ret="+str(retweetList[i].retweet))
        if(  len(retweetList[i].retweet)==0 or  retweetList[i].retweet == None ):
            G.add_node(retweetList[i].user,color='green')

        else:
            for j in range(0,len(retweetList[i].retweet)):
                 # print(retweetList[i].retweet[j],retweetList[i].user)
                 # if probDiz.has_key((retweetList[i].retweet[j],retweetList[i].user)):
                 #    G.add_edge(retweetList[i].retweet[j],retweetList[i].user,weight=probDiz.get((retweetList[i].retweet[j],retweetList[i].user)))
                 # else:
                     G.add_edge(retweetList[i].retweet[j],retweetList[i].user)

    return G

def NodeDict(lista_ret):
    dizionarioNodi= {}
    for i in range (0,len(lista_ret)):
        if not  dizionarioNodi.has_key(lista_ret[i].user):
            dizionarioNodi[lista_ret[i].user] = lista_ret[i].user
        if lista_ret[i].retweet != 0 or lista_ret[i].retweet != None:
                for j in range(0,len(lista_ret[i].retweet)):
                    if not dizionarioNodi.has_key(lista_ret[i].retweet[j]):
                        dizionarioNodi[lista_ret[i].retweet[j]] = lista_ret[i].retweet[j]

    return dizionarioNodi

def PosNode(nodeList,Dict):
    list_pos=[]
    x=0
    for i in nodeList:
       if Dict.has_key(i):
          list_pos.append(x)
          x= x+1
       else:
           x= x+1

    return list_pos

def Polarization(matrix,posRed,posBlue,numNodes):
        DizPolarization = {}
        for i in range(0,numNodes):
            sumRed = 0
            sumBlue = 0
            for j in range(0,numNodes):
                if j in posRed:
                    sumRed= sumRed + matrix.item(i*numNodes +j)
                    #print("sumRed=",sumRed,"i=",i,"j",j)
                elif j in posBlue:
                    sumBlue = sumBlue + matrix.item(i*numNodes +j)
                    #print "sumBlue=",sumBlue,"i=",i,"j",j
            if not DizPolarization.has_key(i):
                if sumBlue == 0 and sumRed ==0:
                    DizPolarization[i] = str(0)
                else:
                    DizPolarization[i]=str(float("{0:.2f}".format(sumBlue-sumRed)))

        return DizPolarization




def main():
    # Leggo il file pickle dei retweet
    # Costruisco un grafo con networkx partendo dai dati ottenuti
    with open('../TweetOldSerialization/pickle/RegionaliSiciliaTest/retweetBlueRegionali Sicilia_2017-09-01_2017-09-15_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)
    #List = retweetList
    with open('../TweetOldSerialization/pickle/RegionaliSiciliaTest/retweetRedRegionali Sicilia_2017-09-01_2017-09-15_data.pkl', 'rb') as input:
        retweetListRed = pickle.load(input)
    with open ('../TweetOldSerialization/pickle/RegionaliSiciliaTest/tweetRegionali Sicilia_2017-09-01_2017-09-15_dictionaryReTweetBlue.pkl', 'rb') as input:
        probRetBlue = pickle.load(input)
    with open('../TweetOldSerialization/pickle/RegionaliSiciliaTest/tweetRegionali Sicilia_2017-09-01_2017-09-15_dictionaryReTweetRed.pkl','rb') as input:
        probRetRed = pickle.load(input)

    with open('../TweetOldSerialization/pickle/RegionaliSiciliaTest/tweetRegionali Sicilia_2017-09-01_2017-09-15_dictionaryReTweetYellow.pkl','rb') as input:
        probYellowGraph = pickle.load(input)

    with open('../TweetOldSerialization/pickle/RegionaliSiciliaTest/retweetYellowRegionali Sicilia_2017-09-01_2017-09-15_data.pkl', 'rb') as input:
        retweetListYellow = pickle.load(input)

    List=[]
    for i in retweetList:
        #ret= Retweet(retweetList[i].user,retweetList[i].retweet, retweetList[i].date)
        print("Blue",i.user,i.retweet, i.date)
        List.append(i)
    for i in retweetListRed:
        #print("Red",i.user,i.retweet, i.date)
        #ret= Retweet(retweetListRed[i].user,retweetListRed[i].retweet, retweetListRed[i].date)
        #print("RED",retweetListRed[i].user,retweetListRed[i].retweet, retweetListRed[i].date)
        List.append(i)

    for i in retweetListYellow:
        List.append(i)

    DizPesi={}

    for i in  probRetBlue:
        print(i)
        #prob = countOccReTweet(probRetBlue[i].edge, probRetBlue[i].count, probRetBlue[i].date)
        #print("Blue",probRetBlue[i].edge, probRetBlue[i].count, probRetBlue[i].date)
        if not DizPesi.has_key(probRetBlue[i].edge):
            DizPesi[probRetBlue[i].edge]= probRetBlue[i].count

    for i in probRetRed:
        #prob = countOccReTweet(probRetRed[i].edge, probRetRed[i].count, probRetRed[i].date)
        #print("RED",probRetRed[i].edge, probRetRed[i].count, probRetRed[i].date)
        if not DizPesi.has_key(probRetRed[i].edge):
            DizPesi[probRetRed[i].edge]= probRetRed[i].count

    for i in probYellowGraph:
        if not DizPesi.has_key(probYellowGraph[i].edge):
            DizPesi[probYellowGraph[i].edge]= probYellowGraph[i].count
    #print(DizPesi)
    nodi_Blue= NodeDict(retweetList)
    nodi_Red = NodeDict(retweetListRed)
    print nodi_Blue
    #G = createUndirectGraph(List)
    G = createGraph(List,DizPesi)
    size_node_degree= []


    posizioneBlue = PosNode(G.nodes(),nodi_Blue)
    posizioneRed = PosNode(G.nodes(),nodi_Red)
   # print("Nodi=",G.nodes())
    #print("Edge=",G.edges(data='weight'))
    print("posRed",posizioneRed)
    print ("posBlue",posizioneBlue)
    print(G.nodes())
    #print("Differenze All-blue",G.nodes()-posizioneBlue)
    #matrice=nx.attr_matrix(G)

    mat = nx.google_matrix(G)
    #print("matrice",matrice)



   #partition = community.best_partition(G)

   # size = float(len(set(partition.values())))

    count = 0.
    #cambio i colori dei nodi a seconda del loro grado
    node_color = []
    Polar = Polarization(mat,posizioneRed,posizioneBlue,len(G.nodes))

    #funziona con i grafi senza partitioning
    for i in range(0,len(G.nodes())):

        if i in posizioneBlue:
           # print i,"yellow",list[i]
            node_color.append('Blue')
        elif i in posizioneRed:
            # print i,"red",list[i]
             node_color.append('red')
        else:
            node_color.append('grey')

    #funziona con la partizione
    node_color_with_partition=[]
    for i in G.nodes():
        if i in nodi_Blue:
            node_color_with_partition.append('Blue')
        elif i in nodi_Red:
            node_color_with_partition.append("Red")
        else:
            node_color_with_partition.append("grey")

    labels={}
    k=0
    for i in G.nodes():
        if Polar.has_key(k):

            labels[i]=Polar.get(k)
            k = k+1
        else:
            k=k+1


    # for node in G.nodes():
    #     print node
    #     if G.degree(node) == 7:
    #         node_color[node]='yellow'
    #     else:
    #         node_color[node]='red'
   #cambio l size dei nodi in basi al grado del nodo
    # size_node=[]
    # for node in G:
    #     if G.degree(node) > 10:
    #         size_node.append(30)
    #     elif G.degree(node) >5 & G.degree(node) <= 10:
    #         size_node.append(8)
    #     elif G.degree(node) >1 & G.degree(node) <= 5:
    #         size_node.append(6)
    #     else:
    #         size_node.append(4)


   # nx.draw(G,pos,nodelist=G.nodes,node_size=20, node_color=node_color, with_labels=True)
    pos = nx.spring_layout(G)
  #Per la partizione
    # list_nodes=[]
    # for com in set(partition.values()):
    #     count = count + 1.
    #     x=0
    #     for nodes in partition.keys():
    #         print "nodes",nodes
    #         if partition[nodes] == com :
    #             list_nodes.append(nodes)


    #con la partizione
    #nx.draw_networkx_nodes(G, pos ,list_nodes,with_labels=False,node_color=node_color_with_partition)

    nx.draw_networkx_nodes(G, pos ,G.nodes(),with_labels=False,node_color=node_color)

    nx.draw_networkx_edges(G, pos, alpha=0.5,edge_color='b')

    nx.draw_networkx_labels(G, pos,labels,font_size=12)

    plt.show()

if __name__ == '__main__':
    main()