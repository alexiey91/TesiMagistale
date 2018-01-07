from __future__ import division
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import community
import numpy as np
import operator
import heapq


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

'''
    @param retweetList: is the list of Nodes with retweet references of one partition of Graph 
    @param probDiz: is the dictionary with the retweet probability  
    @return DiGraph with weight on Edges as retweet probability
'''
def createGraph(retweetList,probDiz,DizCountWeight):
    G = nx.DiGraph()
    #print(retweetList[1][1])
    for i in range(0,len(retweetList)):
       # print ("pos" + str(i)+"username="+ retweetList[i].user +"ret="+str(retweetList[i].retweet))
        if(  len(retweetList[i].retweet)==0 or  retweetList[i].retweet == None ):
            #G.add_node(retweetList[i].user)
         continue

        else:
            for j in range(0,len(retweetList[i].retweet)):
                # print(retweetList[i].retweet[j],retweetList[i].user)
                 if probDiz.has_key((retweetList[i].retweet[j],retweetList[i].user)):
                    G.add_edge(retweetList[i].retweet[j],retweetList[i].user)
                    if not DizCountWeight.has_key(retweetList[i].retweet[j]):
                       DizCountWeight[retweetList[i].retweet[j]]=probDiz[(retweetList[i].retweet[j],retweetList[i].user)]
                       print(retweetList[i].retweet[j], "=",DizCountWeight[retweetList[i].retweet[j]])
                    else:
                        DizCountWeight[retweetList[i].retweet[j]] = DizCountWeight.get(retweetList[i].retweet[j])+probDiz[(retweetList[i].retweet[j], retweetList[i].user)]
                        print("ELSE",retweetList[i].retweet[j],"=",DizCountWeight[retweetList[i].retweet[j]])
                 else:
                     G.add_edge(retweetList[i].retweet[j],retweetList[i].user)

    return G


'''
    @param retweetList: is the list of Nodes with retweet references of one partition of Graph 
    @return Graph without weight on Edges
'''

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

'''
    @param retweetList: is the list of Nodes with retweet references of one partition of Graph 
    @return DiGraph without weight on Edges
'''

def createDirectNoWeightGraph(retweetList):
    G = nx.DiGraph()
    #print(retweetList[1][1])
    for i in range(0,len(retweetList)):
       # print ("pos" + str(i)+"username="+ retweetList[i].user +"ret="+str(retweetList[i].retweet))
        if(  len(retweetList[i].retweet)==0 or  retweetList[i].retweet == None ):
            #G.add_node(retweetList[i].user)
            continue

        else:
            for j in range(0,len(retweetList[i].retweet)):
                 # print(retweetList[i].retweet[j],retweetList[i].user)
                 # if probDiz.has_key((retweetList[i].retweet[j],retweetList[i].user)):
                 #    G.add_edge(retweetList[i].retweet[j],retweetList[i].user,weight=probDiz.get((retweetList[i].retweet[j],retweetList[i].user)))
                 # else:
                     G.add_edge(retweetList[i].retweet[j],retweetList[i].user)

    return G


'''
    @param lista_ret: is the list of Nodes of one partition of Graph 
    @return Dictionary with key as nodes and value nodes of partition (Red/Blue) of Graph   
'''

def NodeDict(lista_ret):
    dizionarioNodi= {}
    for i in range (0,len(lista_ret)):
        if not  dizionarioNodi.has_key(lista_ret[i].user):
            dizionarioNodi[lista_ret[i].user] = lista_ret[i].user
        if lista_ret[i].retweet != 0 or lista_ret[i].retweet != None:
                dizionarioNodi[lista_ret[i].user] = lista_ret[i].user
                for j in range(0,len(lista_ret[i].retweet)):
                    if not dizionarioNodi.has_key(lista_ret[i].retweet[j]):
                        dizionarioNodi[lista_ret[i].retweet[j]] = lista_ret[i].retweet[j]
        else:
            del dizionarioNodi[lista_ret[i].user]

    return dizionarioNodi


'''
    @param nodeList: is the list of Nodes of Graph
    @param Dict: is the dicitionary of Nodes of Red or Blue parts
    @return list of position of nodes for Red or Blue partition of the graph
'''

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

'''
    @param nodeList: is the list of Nodes of Graph
    @param Dict: is the dicitionary of Nodes of Red or Blue parts
    @return dictionary with key as node and value the position of node (in Blue or Red partition) in the graph
'''

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


'''
    @param list_ret: is the list of Nodes with retweet references
    @param dizNodi: is the dicitionary of Nodes 
    @return update the dictionary of Red or Blue group from a list, it use to correct eventual error of machine learning
'''

def UpdateNode(list_ret,dizNodi):
        for i in range (0,len(list_ret)):
            if  dizNodi.has_key(list_ret[i].user):
             if list_ret[i].retweet != 0 or list_ret[i].retweet != None:
                for j in range(0, len(list_ret[i].retweet)):
                 if not dizNodi.has_key(list_ret[i].retweet[j]):
                        dizNodi[list_ret[i].retweet[j]] = list_ret[i].retweet[j]
            else :
                continue



'''
    @param p_array: is the Google Matrix of transaction of Graph as an array
    @param posRed: is the list of position for Red node of Graph
    @param posBlue: is the list of position for Blue node of Graph
    @param numNodes: is the number of Nodes of graph
    @param matrixProbRet: is the matrix of retweet probability of edges
    @return the dictionary of Polarization for all nodes of the Graph
'''

def Polarization(p_array,posRed,posBlue,numNodes,matrixProbRet):
        DizPolarization = {}
        for i in range(0,numNodes):
            sumRed = 0
            sumBlue = 0
            for j in range(0,numNodes):
                if j in posRed:

                    sumRed= sumRed + (p_array[i][j])
                    #print("sumRed=",sumRed,"i=",i,"j",j)
                elif j in posBlue:
                    sumBlue = sumBlue + (p_array[i][j])
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

'''
    @param probDiz: is the dictionary about the probability of retweet 
    @param DizPosRed: is the dictionary with key as Node and value position in the Graph for Red group
    @param DizPosBlue: is the dictionary with key as Node and value position in the Graph for Red group
    @param listNode: is the list of Node with user Retweet
    @param G: is the graph
    @return the matrix of edge with probabbility retweet
'''


def matrixProbRet(probDiz,DizPosRed,DizPosBlue,listNode,G):
    #creo una matrice NxN in base al numero di nodi
    matrice=[[0 for x in range(len(G.nodes()))] for y in range(len(G.nodes()))]
   # print(matrice,len(listaNodi),len(G.node()))
    for i in range (0,len(listNode)):
        if (len(listNode[i].retweet) == 0 or listNode[i].retweet == None):

            continue
        else:
            for j in range(0, len(listNode[i].retweet)):
                # print(retweetList[i].retweet[j],retweetList[i].user)
                if probDiz.has_key((listNode[i].retweet[j], listNode[i].user)):
                    if DizPosBlue.has_key(listNode[i].user) and DizPosBlue.has_key(listNode[i].retweet[j]):
                        #print("ciao",DizPosBlue.get(listaNodi[i].retweet[j]),DizPosBlue.get(listaNodi[i].user),probDiz.get((listaNodi[i].retweet[j], listaNodi[i].user)))
                        matrice[DizPosBlue.get(listNode[i].retweet[j])][DizPosBlue.get(listNode[i].user)] = \
                            probDiz.get((listNode[i].retweet[j], listNode[i].user))

                    elif DizPosRed.has_key(listNode[i].user) and DizPosRed.has_key(listNode[i].retweet[j]):
                        matrice[DizPosRed.get(listNode[i].retweet[j])][DizPosRed.get(listNode[i].user)] = \
                            probDiz.get((listNode[i].retweet[j], listNode[i].user))

    return matrice

'''
    @param PolarDict: is the dictionary of Polarization of Graph
    @param Graph: is a diGraph
    @param node_Blue: is the dictionary of node in Blue group from graph
    @param node_Red: is the dictionary of node in Red group from graph
    @return the list of label of Polarization to draw into the graph nodes
'''

def labelPolarization(PolarDict, Graph, node_Blue, node_Red):
    labels = {}
    k = 0
    for i in Graph.nodes():
        if PolarDict.has_key(k):
            if Graph.out_degree(i) == 0:
                if i in node_Blue:
                    labels[i] = str(1.0)
                elif i in node_Red:
                    labels[i] = str(-1.0)
                else:
                    labels[i] = PolarDict.get(k)

            else:
                labels[i] = PolarDict.get(k)
            k = k + 1
        else:
            k = k + 1

    return labels


'''
    @param Graph: is a diGraph
    @param node_Blue: is the dictionary of node position in Blue group from graph
    @param node_Red: is the dictionary of node position in Red group from graph
    @return the list of color of all nodes graph
'''

def colorNode(Graph,node_Blue,node_Red):
    node_color_with_partition = []
    for i in Graph.nodes():
        if i in node_Blue:
            node_color_with_partition.append('Blue')
        elif i in node_Red:
            node_color_with_partition.append("Red")
        else:
            node_color_with_partition.append("grey")
    return node_color_with_partition


'''
    @param Graph: is a diGraph
    @param node_Blue: is the dictionary of node position in Blue group from graph
    @param node_Red: is the dictionary of node position in Red group from graph
    @return the list of color of all nodes graph
'''

def colorNodePol(lenGraph,Pol):
    node_color_with_partition = []
    for i in range(0,lenGraph):
        print(Pol[i])
        if Pol[i] > 0:
            node_color_with_partition.append('Blue')
        elif Pol[i] < 0:
            node_color_with_partition.append("Red")
        else:
            node_color_with_partition.append("grey")
    return node_color_with_partition

'''
    @param G: is a diGraph
    @param dictNodeBlue: is the dictionary of node position in Blue group from graph
    @param dictNodeRed: is the dictionary of node position in Red group from graph
    @return the list of polarization of node Elite and Listener
'''
def setFirstPolarization(G,dictNodeBlue,dictNodeRed):
    listPolarization=[]
    for i in G.nodes():
        if G.in_degree(i) >0:
            if dictNodeBlue.has_key(i):
                listPolarization.append(+1.)
            elif dictNodeRed.has_key(i):
                listPolarization.append(-1.)
            else:
                listPolarization.append(0.)
        else:
            listPolarization.append(0.)

    return listPolarization


def opinionPolarization(G,attr_mat,firstPol,nodeList):
    newPol=[]
    for i in range(0,len(firstPol)):
        sum=0.
        for j in range(0,len(nodeList)):
            sum= sum+ (attr_mat[i][j]*firstPol[j])
            #print("sum",i," ",sum)

        #dangling
        if G.out_degree(nodeList[i])==0 and sum ==0:
            newPol.append(firstPol[i])
        else:
            newPol.append(sum/float("{0:.2f}".format(G.out_degree(nodeList[i]))))

    return newPol


def opinionPolarizationDict(G,attr_mat,firstPol,nodeList):
    dict={}
    number= divmod(len(nodeList),20)
    #print(len(nodeList),"div=",number[0])
    for i in range(0,number[0]):
        if i ==0:
            dict[i]=firstPol
        else:
            dict[i]=opinionPolarization(G,attr_mat,dict.get(i-1),nodeList)

    return dict

def setWeightEdge(G,DizWeightTot,Dictionary):
    for i in G.edges:
        if DizWeightTot.has_key(i[0]):
            #print(i[0],i[1],"=",Dictionary[(i[0],i[1])]/DizWeightTot[i[0]])
            G[i[0]][i[1]]['weight']=Dictionary[(i[0],i[1])]/DizWeightTot[i[0]]

def deleteList(List1,List2):
    for i in List1:
        for j in List2:
            if i.user == j.user:
                List2.remove(j)


def getAllWeightEdge(DizPesi):
    dizAll = {}
    for i in DizPesi:
        #print(i[0])
        if not dizAll.has_key(i[0]):
            dizAll[i[0]]= DizPesi[i]
        else:
            dizAll[i[0]] = dizAll[i[0]]+DizPesi[i]

    return dizAll

'''
    @param G: is a diGraph
    @param node: is a single node of graph
    @param DizProbRet: is the dictionary of retweet probability with edge as key and p as a value
    @return the dictionary with the node as key and list of probability of its neighbour
'''
def getProbRandomNeighbour(G,node,DizProbRet):
    neighbours = G.neighbors(node)
    #print("vicini del",node,"  ",neighbours);
    arrProb=[]
    for i in neighbours:
       # print i

        for j in DizProbRet:

            if (node,i) == j:

                arrProb.append(DizProbRet[j])

    return arrProb;


def getListNeighbour(G,node):
    neigh = G.neighbors(node)
    listNei=[]

    for i in neigh:

        listNei.append(i)


    return listNei

def dictDegreeNodePart(G,partition):
    dictDegree ={}
    for i in G.nodes():
        if partition.has_key(i):
           dictDegree[i]= G.in_degree(i)

   # newA = dict(sorted(dictDegree.iteritems(), key=dictDegree.get, reverse=True)[:5])
    newA=heapq.nlargest(5, dictDegree, key=dictDegree.get)
    return newA;

def dictDegreeDiscendent(G,node,partition):
    dictDegree = {}
    disc= nx.descendants(G,node)
    for i in disc:
        if partition.has_key(i):
            dictDegree[i] = G.in_degree(i)

    # newA = dict(sorted(dictDegree.iteritems(), key=dictDegree.get, reverse=True)[:5])
    newA = heapq.nlargest(5, dictDegree, key=dictDegree.get)
    print newA
    return newA;

def release_list(a):
   del a[:]
   del a

#EdgeProb e' il dizionario di ogni nodo con la lista delle probabilita
#DizProbRet sono gli archi come chiave con le prob di retweet
def performRandomWalkSingleNode(G,startnode,listNodeBlueDegree,listNodeRedDegree,num_walk,Red,Blue,EdgeProb,DizProbRet):
    tempBlue= startnode
    tempRed = startnode
    resultBlue={}
    resultRed={}
    resultPol={}
    visited_nodeRed=[]
    counterPolRed = 1.
    visited_nodeBlue = []
    counterPolBlue = 1.
    restartBlue= True
    restartRed = True
    '''
    numero di tentantivi per raggiungere il nodo i e' il contatore dei passi verso i nodi di grado max blue
    '''
    print startnode
    while restartBlue:
        restartBlue= False
        for i in range(0,num_walk):
            print("tempBlue", tempBlue)
            print("i", i)

            if bool(listNodeBlueDegree)== False:
                counterPolBlue = 0.
                resultBlue[startnode] = (counterPolBlue,"nessunBlue")
                break
            if i== 0:
                visited_nodeBlue.append(tempBlue)
            #ListNeighbours = G.neighbors(tempBlue)
            ListNeighboursBlue = getListNeighbour(G,tempBlue)
            print "Vicini",ListNeighboursBlue
            if bool(ListNeighboursBlue) == False:
                if i==0:
                    print("i==0")
                    counterPolBlue = 1.
                    resultBlue[startnode] = (counterPolBlue, visited_nodeBlue)
                    break

                elif successorNodeBlue not in listNodeBlueDegree:
                    print("SuccessorNode non in listBlue",i,counterPolBlue,tempBlue,visited_nodeBlue)
                    #counterPolBlue = 0.
                    #resultBlue[startnode] = (counterPolBlue, visited_nodeBlue)
                    #break
                    counterPolBlue = 0.
                    tempBlue = startnode
                    release_list(visited_nodeBlue)
                    print "Ricomincio",i,counterPolBlue,tempBlue,visited_nodeBlue
                    restartBlue = True
                    break


                else:
                    print("successore blue esco")
                    resultBlue[startnode] = (counterPolBlue, visited_nodeBlue)
                    break

            else:
                ListProbBlue = getProbRandomNeighbour(G,tempBlue,DizProbRet)
                print "ListProbBlue", ListProbBlue

                successorNodeBlue=np.random.choice(ListNeighboursBlue, 1, p=ListProbBlue)[0]
                #successorNode = ListNeighbours[randomNode]
                print "successorNodeBlue" ,successorNodeBlue

                if successorNodeBlue in listNodeBlueDegree:
                    print "Succesore in lista DegreeBlue"
                    visited_nodeBlue.append(successorNodeBlue)

                    resultBlue[startnode]=(counterPolBlue,visited_nodeBlue)
                    break

                elif i == num_walk:
                        print "dentro i = numWalk", i
                        if successorNodeBlue not in listNodeBlueDegree:
                            counterPolBlue= 1.
                            resultBlue[startnode]=(counterPolBlue,visited_nodeBlue)
                else:
                    print "i", i
                    if tempBlue != successorNodeBlue:
                        visited_nodeBlue.append(successorNodeBlue)
                    print  "ELSEBlue=", DizProbRet[(tempBlue, successorNodeBlue)], visited_nodeBlue
                    #counterPolBlue=counterPolBlue*EdgeProb[(tempBlue,successorNode)]
                    counterPolBlue=counterPolBlue*DizProbRet[(tempBlue,successorNodeBlue)]
                    tempBlue = successorNodeBlue
                    print tempBlue

    print "fine Blue",counterPolBlue
    while restartRed:
        restartRed= False
        for i in range(0,num_walk):
            print("tempRed",tempRed)
            print("i",i)
            if i== 0:
                visited_nodeRed.append(tempRed)

            if bool(listNodeRedDegree)== False:
                counterPolRed = 0.
                resultRed[startnode] = (counterPolRed,"Nessun Red")
                break
            #ListNeighbours = G.neighbors(tempBlue)
            ListNeighboursRed = getListNeighbour(G,tempRed)
            print "Vicini",ListNeighboursRed
            if bool(ListNeighboursRed) == False:
                if i==0:
                    print("i==0")
                    counterPolRed = 1.
                    resultRed[startnode] = (counterPolRed, visited_nodeRed)
                    break
                elif successorNodeRed not in listNodeRedDegree:
                    print("SuccessorNode non in listRed",i,counterPolRed,tempRed,visited_nodeRed)
                    #counterPolRed = 0.
                    #resultRed[startnode] = (counterPolRed, visited_nodeRed)
                    #break
                    counterPolRed = 1.
                    tempRed = startnode
                    release_list(visited_nodeRed)
                    print "Ricomincio", i, counterPolRed, tempRed, visited_nodeRed
                    restartRed = True

                else:
                    print()
                    resultRed[startnode] = (counterPolRed, visited_nodeRed)
                    break
            else:
                ListProbRed = getProbRandomNeighbour(G,tempRed,DizProbRet)
                print "ListProbRed",ListProbRed
                successorNodeRed=np.random.choice(ListNeighboursRed, 1, p=ListProbRed)[0]
                #successorNode = ListNeighbours[randomNode]
                print "successorNodeRed" ,successorNodeRed
                if successorNodeRed in listNodeRedDegree:
                    print "Succesore in lista DegreeRed"
                    visited_nodeRed.append(successorNodeRed)

                    resultRed[startnode]=(counterPolRed,visited_nodeRed)
                    break

                elif i == num_walk:
                    print "dentro i = ",i
                    if successorNodeRed not in listNodeRedDegree:
                        counterPolRed= 0.
                        resultRed[startnode]=(counterPolRed,visited_nodeRed)


                else:
                    print "i",i
                    if tempRed != successorNodeRed:
                        visited_nodeRed.append(successorNodeRed)

                    print  "ELSERed=",DizProbRet[(tempRed,successorNodeRed)],visited_nodeRed
                    #counterPolRed=counterPolRed*EdgeProb[(tempRed,successorNode)]
                    counterPolRed = counterPolRed * DizProbRet[(tempRed, successorNodeRed)]
                    tempRed = successorNodeRed



    print "Fine red",counterPolRed
    print "resultBlue[0]",
    print "ListaBlue visitate",resultBlue[startnode]
    print "ListaRed visitate",resultRed[startnode]
    diffPol = resultBlue[startnode][0]-resultRed[startnode][0]
    print "diffPol",diffPol
    resultPol[startnode]=(diffPol,resultBlue[startnode][1],resultRed[startnode][1])

    return resultPol





def main():
    # Leggo il file pickle dei retweet
    # Costruisco un grafo con networkx partendo dai dati ottenuti
    with open('../TweetOldSerialization/pickle/#EleSiciliaTestAWS/retweetBlue#EleSicilia_2017-09-01_2017-09-15_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)
    #List = retweetList
    with open('../TweetOldSerialization/pickle/#EleSiciliaTestAWS/retweetRed#EleSicilia_2017-09-01_2017-09-15_data.pkl', 'rb') as input:
        retweetListRed = pickle.load(input)
    with open ('../TweetOldSerialization/pickle/#EleSiciliaTestAWS/tweet#EleSicilia_2017-09-01_2017-09-15_dictionaryReTweetBlue.pkl', 'rb') as input:
        probRetBlue = pickle.load(input)
    with open('../TweetOldSerialization/pickle/#EleSiciliaTestAWS/tweet#EleSicilia_2017-09-01_2017-09-15_dictionaryReTweetRed.pkl','rb') as input:
        probRetRed = pickle.load(input)

    with open('../TweetOldSerialization/pickle/#EleSiciliaTestAWS/tweet#EleSicilia_2017-09-01_2017-09-15_dictionaryReTweetYellow.pkl','rb') as input:
        probYellowGraph = pickle.load(input)

    with open('../TweetOldSerialization/pickle/#EleSiciliaTestAWS/retweetYellow#EleSicilia_2017-09-01_2017-09-15_data.pkl', 'rb') as input:
        retweetListYellow = pickle.load(input)

    deleteList(retweetList,retweetListRed)

    List=[]
    for i in retweetList:
        #ret= Retweet(retweetList[i].user,retweetList[i].retweet, retweetList[i].date)
       # print("Blue",i.user,i.retweet, i.date)
        List.append(i)
    for i in retweetListRed:
        #print("Red",i.user,i.retweet, i.date)
        #ret= Retweet(retweetListRed[i].user,retweetListRed[i].retweet, retweetListRed[i].date)
        #print("RED",retweetListRed[i].user,retweetListRed[i].retweet, retweetListRed[i].date)
        List.append(i)

    # for i in retweetListYellow:
    #     # print("Red",i.user,i.retweet, i.date)
    #      List.append(i)


    DizPesi={}

    for i in  probRetBlue:
        #print('Blue',i.edge,i.count)
        #prob = countOccReTweet(probRetBlue[i].edge, probRetBlue[i].count, probRetBlue[i].date)
       # print("Blue",probRetBlue[i].edge, probRetBlue[i].count, probRetBlue[i].date)
        if not DizPesi.has_key(probRetBlue[i].edge):
            DizPesi[probRetBlue[i].edge]= probRetBlue[i].count
        else:
            continue

    for i in probRetRed:
       # prob = countOccReTweet(probRetRed[i].edge, probRetRed[i].count, probRetRed[i].date)
        #print("RED",probRetRed[i].edge, probRetRed[i].count, probRetRed[i].date)
        if not DizPesi.has_key(probRetRed[i].edge):
            DizPesi[probRetRed[i].edge]= probRetRed[i].count
        else:
            continue

    # for i in probYellowGraph:
    #     if not DizPesi.has_key(probYellowGraph[i].edge):
    #         DizPesi[probYellowGraph[i].edge]= probYellowGraph[i].count
    #print(DizPesi)

    #deleteProbDiz(DizPesi)
    #print("DizPesi",DizPesi,len(DizPesi))
    nodi_Blue= NodeDict(retweetList)
    nodi_Red = NodeDict(retweetListRed)
    #nodi_Yellow = NodeDict(retweetListYellow)
    print ("Blue",nodi_Blue,len(nodi_Blue))
    print ("Red", nodi_Red,len(nodi_Blue))
    #G = createUndirectGraph(List)
    DizionarioPesiArchi={}
    #G = createGraph(List,DizPesi,DizionarioPesiArchi)
    G = createDirectNoWeightGraph(List)
    size_node_degree= []
    G.add_edge(u'beppevicari', 'claudioreale')
    #G.add_edge('claudioreale','OpenGDB')

    DizPesi[(u'beppevicari', 'claudioreale')]=2
    #DizPesi[('claudioreale','OpenGDB')]=2
    NumberRetweetDiz = getAllWeightEdge(DizPesi)
    #print NumberRetweetDiz
    UpdateNode(retweetListYellow,nodi_Blue)
    UpdateNode(retweetListYellow,nodi_Red)

    setWeightEdge(G, NumberRetweetDiz, DizPesi)
    #print(test)

    posizioneBlue = PosNode(G.nodes(),nodi_Blue)
    posizioneRed = PosNode(G.nodes(),nodi_Red)
    #posizioneYellow = PosNode(G.nodes(),nodi_Yellow)
    dizPosizioneBlue=PosNodeDizionario(G.nodes,nodi_Blue)
    dizPosizioneRed=PosNodeDizionario(G.nodes,nodi_Red)
    #dizPosizioneYellow = PosNodeDizionario(G.nodes,nodi_Yellow);
    # print("Nodi=",G.nodes())
    print("DizPosBlue",dizPosizioneBlue)
    print("DizPosRed",dizPosizioneRed)
    # print("DizPosYelloq",dizPosizioneYellow)
    #print("Edge=",G.edges(data='weight'))
    #print("posRed",posizioneRed)
    #print ("posBlue",posizioneBlue)
    #print(G.nodes())
    #print("Differenze All-blue",G.nodes()-posizioneBlue)

    #matriceProbRetweet= matrixProbRet(DizPesi,dizPosizioneRed,dizPosizioneBlue,List,G)

    #List of Polarization of Elite and Listener
    firstPolar= setFirstPolarization(G,dizPosizioneBlue,dizPosizioneRed)

    #print "Passo 0 di polarizzazione ",firstPolar

    dictFirstPol = {}
    x = 0
    for i in G.nodes():

        if not dictFirstPol.has_key(i):
            dictFirstPol[i] = firstPolar[x]
            x = x + 1


    list = []
    for i in G.nodes():

        list.append(i)


    #matrice di adiacenza partendo dalla lista dei nodi
    mat_attr=nx.attr_matrix(G,rc_order=list)
    #print(mat_attr[1])

    at_array=np.array(mat_attr)

    newPol=opinionPolarization(G,at_array,firstPolar,list)

    dictPol={}
    x=0
    for i in G.nodes():

        if not dictPol.has_key(i):
            dictPol[i]=newPol[x]
            x=x+1

   #settare i vertici dangling
    #matrice=nx.google_matrix(G,alpha=1)
    #p_array = np.array(matrice)

    #print matrice,len(matrice),matrice[131]
    # sumBlue=0.
    # sumRed = 0.
    # sumYellow =0.
    # count =0;
    # for i in range(0,len(p_array)):
    #     if i in posizioneBlue:
    #         sumBlue = sumBlue + p_array[15][i]
    #         count = count+1
    #
    #     elif i in posizioneRed:
    #         sumRed = sumRed +  p_array[15][i]
    #         # print "sumBlue=",sumBlue,"i=",i,"j",j
    #     elif i in posizioneYellow:
    #         sumYellow= sumYellow + p_array[15][i]

    #print p_array[15],"sumBlue",sumBlue,"sumRed",sumRed,"sumYellow",sumYellow,count,len(posizioneBlue),mat_attr


    partition = community.best_partition(G.to_undirected())
   # print(partition)

    #print(len(G.nodes))
    #size = float(len(set(partition.values())))

    count = 0.
    #cambio i colori dei nodi a seconda del loro grado
    #Polar = Polarization(p_array,posizioneRed,posizioneBlue,len(G.nodes),matriceProbRetweet)

    #funziona con la partizione
    node_color= colorNode(G,nodi_Blue,nodi_Red)

    #node_colorPol= colorNodePol(len(G.nodes()),newPol)


    testdict=opinionPolarizationDict(G,at_array,firstPolar,list)
    #print(testdict)
    list_lastPol=testdict.get(len(testdict)-1)
    #print(list_lastPol)
    #print(set(testdict[1]))
   # node_colorPol=colorNodePol(len(G.nodes()),list_lastPol)

    # test = {}
    # x = 0
    # for i in G.nodes():
    #
    #     if not testdict.has_key(i):
    #         test[i] = testdict.get(len(testdict)-1)[x]
    #         x = x + 1


    # for i in range(0,len(testdict)):
    #     if i+1 == (len(testdict)-1):
    #         break
    #     print("i",i,"j",i+1," simili=", set(testdict[i])==set(testdict[i+1]))
    #

    #labels= labelPolarization(Polar,G,nodi_Blue,nodi_Red)

    pos = nx.spring_layout(G)
  #Per la partizione
    # list_nodes=[]
    # for com in set(partition.values()):
    #     count = count + 1.
    #     x=0
    #     for nodes in partition.keys():
    #        # print "nodes",nodes
    #         if partition[nodes] == com :
    #             list_nodes.append(nodes)


    #con la partizione
    #nx.draw_networkx_nodes(G, pos ,list_nodes,with_labels=False,node_color=node_color)

    edgeWeightLabel = nx.get_edge_attributes(G, 'weight')
    print("pesi archi",edgeWeightLabel)

    dictTest={}

    for i in G.nodes():
        if not dictTest.has_key(i):
            dictTest[i]= getProbRandomNeighbour(G,i,edgeWeightLabel)

    print("dictgetProbRandom",dictTest)

    dictDegreeBlue= dictDegreeNodePart(G,nodi_Blue)
    print "ListaNodiGradiBlu",dictDegreeBlue


    dictDegreeRed = dictDegreeNodePart(G,nodi_Red)
    result={}
    for i in G.nodes():
        print nx.descendants(G, i)
        dictDegreeDiscRed = dictDegreeDiscendent(G,i,nodi_Red)
        dictDegreeDiscBlue = dictDegreeDiscendent(G,i,nodi_Blue)
        #for j in range(0,5):
         #result.append((j,performRandomWalkSingleNode(G,i,dictDegreeBlue,dictDegreeRed,10,'','',dictTest,edgeWeightLabel)))
          #print "result",result
        result[i]= performRandomWalkSingleNode(G,i,dictDegreeDiscBlue,dictDegreeDiscRed,10,"","",dictTest,edgeWeightLabel)
        #break

    print result,len(result)
    nx.draw_networkx_nodes(G, pos ,G.nodes(),with_labels=True,node_color=node_color)

    nx.draw_networkx_edges(G, pos,edge_labels=edgeWeightLabel,font_size=10,edge_color='b')

    nx.draw_networkx_labels(G, pos,font_size=8)

    plt.savefig("../Test/Sicilia/PolSenzaY.png", format="PNG")

    plt.show()




if __name__ == '__main__':
    main()