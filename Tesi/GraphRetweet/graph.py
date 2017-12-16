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
            G.add_node(retweetList[i].user)

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
            G.add_node(retweetList[i].user)

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
          #print(i,"pos=",x-1)
       else:
           x= x+1

    return list_pos

def PosNodeDizionario(nodeList,Dict):
    list_pos={}
    x=0
    for i in nodeList:
       if Dict.has_key(i):
          list_pos[i]=x
          x= x+1
          #print(i,"pos=",x-1)
       else:
           x= x+1

    return list_pos



def UpdateNode(list_ret,dizNodi):
        for i in range (0,len(list_ret)):
            if  dizNodi.has_key(list_ret[i].user):
             if list_ret[i].retweet != 0 or list_ret[i].retweet != None:
                for j in range(0, len(list_ret[i].retweet)):
                 if not dizNodi.has_key(list_ret[i].retweet[j]):
                        dizNodi[list_ret[i].retweet[j]] = list_ret[i].retweet[j]
            else :
                continue

        #return dizNodi


def Polarization(p_array,posRed,posBlue,numNodes,matriceProbRet):
        DizPolarization = {}
        for i in range(0,numNodes):
            sumRed = 0
            sumBlue = 0
            for j in range(0,numNodes):
                if j in posRed:

                    sumRed= sumRed + (p_array[i][j]*matriceProbRet[i][j])
                    #print("sumRed=",sumRed,"i=",i,"j",j)
                elif j in posBlue:
                    sumBlue = sumBlue + (p_array[i][j]*matriceProbRet[i][j])
                    #print "sumBlue=",sumBlue,"i=",i,"j",j
                else:
                    continue

            if not DizPolarization.has_key(i):
                if sumBlue == 0 and sumRed ==0:
                    DizPolarization[i] = str(0)
                else:
                    if(min(1,sumBlue-sumRed)==1):
                     DizPolarization[i]=str(1.0)
                    elif (max(-1,sumBlue-sumRed)== -1):
                     DizPolarization[i]=str(-1.0)
                    else:
                     DizPolarization[i]=str(float("{0:.2f}".format(sumBlue-sumRed)))

        return DizPolarization



def matrixProbRet(probDiz,DizPosRed,DizPosBlue,listaNodi,G):
    #creo una matrice NxN in base al numero di nodi
    matrice=[[0 for x in range(len(G.nodes()))] for y in range(len(G.nodes()))]
   # print(matrice,len(listaNodi),len(G.node()))
    for i in range (0,len(listaNodi)):
        if (len(listaNodi[i].retweet) == 0 or listaNodi[i].retweet == None):
           #se ho nodi isolati imposto la riga tutta a zero sia se Blu che rosso
           #for j in range(0,len(listaNodi)):
           #   matrice[i][j]=0
            continue
        else:
            for j in range(0, len(listaNodi[i].retweet)):
                # print(retweetList[i].retweet[j],retweetList[i].user)
                if probDiz.has_key((listaNodi[i].retweet[j], listaNodi[i].user)):
                    if DizPosBlue.has_key(listaNodi[i].user) and DizPosBlue.has_key(listaNodi[i].retweet[j]):
                        #print("ciao",DizPosBlue.get(listaNodi[i].retweet[j]),DizPosBlue.get(listaNodi[i].user),probDiz.get((listaNodi[i].retweet[j], listaNodi[i].user)))
                        matrice[DizPosBlue.get(listaNodi[i].retweet[j])][DizPosBlue.get(listaNodi[i].user)] = \
                            probDiz.get((listaNodi[i].retweet[j], listaNodi[i].user))

                    elif DizPosRed.has_key(listaNodi[i].user) and DizPosRed.has_key(listaNodi[i].retweet[j]):
                        matrice[DizPosRed.get(listaNodi[i].retweet[j])][DizPosRed.get(listaNodi[i].user)] = \
                            probDiz.get((listaNodi[i].retweet[j], listaNodi[i].user))

    return matrice


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
        #print(i.edge,i.count)
        #prob = countOccReTweet(probRetBlue[i].edge, probRetBlue[i].count, probRetBlue[i].date)
        print("Blue",probRetBlue[i].edge, probRetBlue[i].count, probRetBlue[i].date)
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
    nodi_Yellow = NodeDict(retweetListYellow)
    #print nodi_Blue
    #G = createDirectNoWeightGraph(List)
    G = createGraph(List,DizPesi)
    size_node_degree= []


    UpdateNode(retweetListYellow,nodi_Blue)
    UpdateNode(retweetListYellow,nodi_Red)
    #print(test)

    posizioneBlue = PosNode(G.nodes(),nodi_Blue)
    posizioneRed = PosNode(G.nodes(),nodi_Red)
    posizioneYellow = PosNode(G.nodes(),nodi_Yellow)
    dizPosizioneBlue=PosNodeDizionario(G.nodes,nodi_Blue)
    dizPosizioneRed=PosNodeDizionario(G.nodes,nodi_Red)

    print("Nodi=",G.nodes())
    print("DizPosBlue",dizPosizioneBlue)
    print("DizPosRed",dizPosizioneRed)
    #print("Edge=",G.edges(data='weight'))
    #print("posRed",posizioneRed)
    #print ("posBlue",posizioneBlue)
    #print(G.nodes())
    #print("Differenze All-blue",G.nodes()-posizioneBlue)

    matriceProbRetweet= matrixProbRet(DizPesi,dizPosizioneRed,dizPosizioneBlue,List,G)

    # print "matriceProbRetweet=",matriceProbRetweet
    # print "riga 9",matriceProbRetweet[9]
    # print "riga 20", matriceProbRetweet[20]
    # print("riga 18",matriceProbRetweet[18])
    # print "riga 32",matriceProbRetweet[32]
    # print ("riga 25",matriceProbRetweet[25])
    # print ("riga 27",matriceProbRetweet[27])
    # print ("riga 19",matriceProbRetweet[19])
    # print ("riga 17",matriceProbRetweet[17])
    # print ("riga 0",matriceProbRetweet[0])
    # print ("riga 15",matriceProbRetweet[15])


    #dumping vector della matrice
    array={}
    for i in range(0,len(G.nodes())):
        array[i]=0


    for r in  posizioneRed:
        array[r] = -(1/len(G.nodes()))

    for b in posizioneBlue:
        array[b] = 1/len(G.nodes())


    #print(array)
    matrice=nx.google_matrix(G,alpha=1)
    p_array = np.array(matrice)

    #print matrice,len(matrice),matrice[131]
    sumBlue=0.
    sumRed = 0.
    sumYellow =0.
    count =0;
    for i in range(0,len(p_array)):
        if i in posizioneBlue:
            sumBlue = sumBlue + p_array[32][i]*matriceProbRetweet[32][i]
            count = count+1

        elif i in posizioneRed:
            sumRed = sumRed +  p_array[32][i]*p_array[32][i]*matriceProbRetweet[32][i]
            # print "sumBlue=",sumBlue,"i=",i,"j",j
        elif i in posizioneYellow:
            sumYellow= sumYellow + p_array[32][i]*p_array[32][i]*matriceProbRetweet[32][i]

    #print p_array[32],"sumBlue",sumBlue,"sumRed",sumRed,"sumYellow",sumYellow,count,len(posizioneBlue)

    mat = nx.google_matrix(G)
    #print("matrice",mat[98])



    #partition = community.best_partition(G)

    #size = float(len(set(partition.values())))

    count = 0.
    #cambio i colori dei nodi a seconda del loro grado
    node_color = []
    Polar = Polarization(p_array,posizioneRed,posizioneBlue,len(G.nodes),matriceProbRetweet)

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
            if G.out_degree(i) == 0:
                if i in nodi_Blue:
                 labels[i] = str(1.0)
                elif i in nodi_Red:
                    labels[i]= str(-1.0)
                else:
                    labels[i] = Polar.get(k)

            else:
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

    nx.draw_networkx_nodes(G, pos ,G.nodes(),with_labels=True,node_color=node_color)

    nx.draw_networkx_edges(G, pos, alpha=0.5,edge_color='b')

    nx.draw_networkx_labels(G, pos,labels,font_size=12)

    plt.show()

if __name__ == '__main__':
    main()