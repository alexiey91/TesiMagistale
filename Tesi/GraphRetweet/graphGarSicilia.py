from __future__ import division
import pickle
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
        if not  dizionarioNodi.has_key(lista_ret[i].user) :
            dizionarioNodi[lista_ret[i].user] = lista_ret[i].user
        if lista_ret[i].retweet != 0 or lista_ret[i].retweet != None:
                dizionarioNodi[lista_ret[i].user] = lista_ret[i].user
                for j in range(0,len(lista_ret[i].retweet)):
                    if not dizionarioNodi.has_key(lista_ret[i].retweet[j]):
                        dizionarioNodi[lista_ret[i].retweet[j]] = lista_ret[i].retweet[j]
        else:
            del dizionarioNodi[lista_ret[i].user]

    return dizionarioNodi

def NodeDictDel(Dict1,Dict2):
    for i in Dict1:
        if Dict2.has_key(i):
            del Dict2[i]

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

            #print(i[0],i[1],"=",Dictionary[(i[0],i[1])],"/",DizWeightTot[i[0]])
            G[i[0]][i[1]]['weight']=Dictionary[(i[0],i[1])]/DizWeightTot[i[0]]
        else:
            continue

def deleteList(List1,List2):
    for i in List1:
        for j in List2:

            if i.user == j.user:

                List2.remove(j)


def deleteList2( List1,List2):
    for el in List1:
      #print(el.user)
      x=list(filter(lambda a: a.user != el.user, List2))
    List2=x
    return List2

def deleteList3 ( List1,List2):
    for i in List1:
        result = [c for c in List2 if c.user == i.user]
        #print("Result",result)
    return result



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


        if sum(arrProb) < 1.0:
            arrProb[len(arrProb)-1] = arrProb[len(arrProb)-1]+ (1-sum(arrProb))

        elif sum(arrProb) > 1.0:
            index, value = max(enumerate(arrProb), key=operator.itemgetter(1))
            somma = 0.
            for i in range(0,len(arrProb)):
              if i!= index:
               somma = somma + arrProb[i]

            arrProb[index]= 1-somma



    return arrProb;

'''
    @param G: is a diGraph
    @param node: is a single node of graph
    @return the list with the node neighbour
'''

def getListNeighbour(G,node):
    neigh = G.neighbors(node)
    listNei=[]

    for i in neigh:

        listNei.append(i)


    return listNei

'''
    @param G: is a diGraph
    @param partition: is a dictionary of partition of graph
    @return the dictionary with the node with best 5 highdegree
'''
def dictDegreeNodePart(G,partition):
    dictDegree ={}
    for i in G.nodes():
        if partition.has_key(i):
           dictDegree[i]= G.in_degree(i)

   # newA = dict(sorted(dictDegree.iteritems(), key=dictDegree.get, reverse=True)[:5])
    newA=heapq.nlargest(5, dictDegree, key=dictDegree.get)
    return newA;


'''
    @param G: is a diGraph
    @param node: is a single node
    @param partition: is a dictionary of partition of graph
    @return the dictionary with the node with best 5 highdegree in the partition
'''
def dictDegreeDiscendent(G,node,partition):
    dictDegree = {}
    disc= nx.descendants(G,node)
    for i in disc:
        if partition.has_key(i):
            dictDegree[i] = G.in_degree(i)

    # newA = dict(sorted(dictDegree.iteritems(), key=dictDegree.get, reverse=True)[:5])
    newA = heapq.nlargest(5, dictDegree, key=dictDegree.get)
   # print newA
    return newA;

def release_list(a):
   del a[:]
   del a

'''
    @param G: is a diGraph
    @param startnode: the start node
    @param listNodeBlueDegree: the list of best 5 high degree of Blue partiotion
    @param listNodeRedDegree: the list of best 5 high degree of Red partiotion
    @param num_walk: number of max hop to exit from algorithm
    @param DizProbRet: is a dictionary of retweet probability woth edge as key
    @return the dictionary with the node as key and its polarization as value
'''
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
    #print startnode
    while restartBlue:
        restartBlue= False
        for i in range(0,num_walk):
            #print("tempBlue", tempBlue)
            #print("i", i)

            if bool(listNodeBlueDegree)== False:
                counterPolBlue = 0.
                resultBlue[startnode] = (counterPolBlue,"nessunBlue")
                break
            if i== 0:
                visited_nodeBlue.append(tempBlue)

            ListNeighboursBlue = getListNeighbour(G,tempBlue)
            #print "Vicini",ListNeighboursBlue
            if bool(ListNeighboursBlue) == False:
                if i==0:
                    #print("i==0")
                    counterPolBlue = 1.
                    resultBlue[startnode] = (counterPolBlue, visited_nodeBlue)
                    break

                elif successorNodeBlue not in listNodeBlueDegree:
                    #print("SuccessorNode non in listBlue",i,counterPolBlue,tempBlue,visited_nodeBlue,successorNodeBlue)

                    counterPolBlue = 1.
                    tempBlue = startnode
                    successorNodeBlue = None
                    release_list(visited_nodeBlue)
                    #print "Ricomincio",i,counterPolBlue,tempBlue,visited_nodeBlue,successorNodeBlue
                    restartBlue = True
                    break


                else:
                    #print("successore blue esco")
                    counterPolBlue = counterPolBlue * DizProbRet[(tempBlue, successorNodeBlue)]
                    resultBlue[startnode] = (counterPolBlue, visited_nodeBlue)
                    break

            else:
                ListProbBlue = getProbRandomNeighbour(G,tempBlue,DizProbRet)
                #print "ListProbBlue", ListProbBlue

                successorNodeBlue=np.random.choice(ListNeighboursBlue, 1, p=ListProbBlue)[0]
                #print "successorNodeBlue" ,successorNodeBlue

                if successorNodeBlue in listNodeBlueDegree:
                    #print "Succesore in lista DegreeBlue"
                    counterPolBlue = counterPolBlue * DizProbRet[(tempBlue, successorNodeBlue)]
                    visited_nodeBlue.append(successorNodeBlue)

                    resultBlue[startnode]=(counterPolBlue,visited_nodeBlue)
                    break

                elif i == num_walk-1:
                        #print "dentro i = numWalk", i
                        if successorNodeBlue not in listNodeBlueDegree:
                            # counterPolBlue= 1.
                            # resultBlue[startnode]=(counterPolBlue,visited_nodeBlue)
                            counterPolBlue = 1.
                            tempBlue = startnode
                            successorNodeBlue = None
                            release_list(visited_nodeBlue)
                            #print "Ricomincio numwalk Blue", i, counterPolBlue, tempBlue, visited_nodeBlue, successorNodeBlue
                            restartBlue = True
                            break

                        else:
                            counterPolBlue = counterPolBlue * DizProbRet[(tempBlue, successorNodeBlue)]
                            visited_nodeBlue.append(successorNodeBlue)

                            resultBlue[startnode] = (counterPolBlue, visited_nodeBlue)
                else:
                    #print "i", i
                    if tempBlue != successorNodeBlue:
                        visited_nodeBlue.append(successorNodeBlue)
                    #print  "ELSEBlue=", DizProbRet[(tempBlue, successorNodeBlue)], visited_nodeBlue

                    counterPolBlue=counterPolBlue*DizProbRet[(tempBlue,successorNodeBlue)]
                    tempBlue = successorNodeBlue
                    #print tempBlue

    #print "fine Blue",counterPolBlue
    while restartRed:
        restartRed= False
        for i in range(0,num_walk):
            #print("tempRed",tempRed)
            #print("i",i)
            if i== 0:
                visited_nodeRed.append(tempRed)

            if bool(listNodeRedDegree)== False:
                #print("nessun listNodeRedDegree")
                counterPolRed = 0.
                resultRed[startnode] = (counterPolRed,"Nessun Red")
                break

            ListNeighboursRed = getListNeighbour(G,tempRed)
            #print "Vicini",ListNeighboursRed
            if bool(ListNeighboursRed) == False:
                if i==0:
                    #print("i==0")
                    counterPolRed = 1.
                    resultRed[startnode] = (counterPolRed, visited_nodeRed)
                    break
                elif successorNodeRed not in listNodeRedDegree:
                    #print("SuccessorNode non in listRed",i,counterPolRed,tempRed,visited_nodeRed,successorNodeRed)


                    counterPolRed = 1.
                    tempRed = startnode
                    successorNodeRed= None
                    #print "Ricomincio", i, counterPolRed, tempRed, visited_nodeRed,successorNodeRed
                    restartRed = True
                    release_list(visited_nodeRed)
                    break

                else:
                    #print("successore rosso esco")
                    counterPolRed = counterPolRed * DizProbRet[(tempRed, successorNodeRed)]
                    resultRed[startnode] = (counterPolRed, visited_nodeRed)
                    break
            else:
                ListProbRed = getProbRandomNeighbour(G,tempRed,DizProbRet)
                #print "ListProbRed",ListProbRed
                successorNodeRed=np.random.choice(ListNeighboursRed, 1, p=ListProbRed)[0]

                #print "successorNodeRed" ,successorNodeRed
                if successorNodeRed in listNodeRedDegree:
                    #print "Succesore in lista DegreeRed"
                    counterPolRed = counterPolRed * DizProbRet[(tempRed, successorNodeRed)]

                    visited_nodeRed.append(successorNodeRed)

                    resultRed[startnode]=(counterPolRed,visited_nodeRed)
                    break

                elif i == num_walk-1:
                    #print "dentro i = ",i
                    if successorNodeRed not in listNodeRedDegree:
                        # counterPolRed= 0.
                        # resultRed[startnode]=(counterPolRed,visited_nodeRed)
                        counterPolRed = 1.
                        tempRed = startnode
                        successorNodeRed = None
                        #print "Ricomincio dopo num_walk passi", i, counterPolRed, tempRed, visited_nodeRed, successorNodeRed
                        restartRed = True
                        release_list(visited_nodeRed)
                        break
                    else:
                        counterPolRed = counterPolRed * DizProbRet[(tempRed, successorNodeRed)]
                        visited_nodeRed.append(successorNodeRed)
                        resultRed[startnode] = (counterPolRed, visited_nodeRed)
                        #print("ultimo passo")

                else:
                    #print "i",i
                    if tempRed != successorNodeRed:
                        visited_nodeRed.append(successorNodeRed)

                    #print  "ELSERed=",DizProbRet[(tempRed,successorNodeRed)],visited_nodeRed
                    counterPolRed = counterPolRed * DizProbRet[(tempRed, successorNodeRed)]
                    tempRed = successorNodeRed



    #print "Fine red",counterPolRed
    # print "Blue",resultBlue[startnode][0]
    # print "Red",counterPolRed, successorNodeRed, resultRed[startnode][0]

    diffPol = resultBlue[startnode][0]-resultRed[startnode][0]

    if diffPol == 0.0 and resultBlue[startnode][1]=='nessunBlue' and resultRed[startnode][1]== 'Nessun Red':
            if Red.has_key(startnode):
                diffPol = -1.0
            else:
                diffPol = 1.0

    resultPol[startnode]=(diffPol,resultBlue[startnode][1],resultRed[startnode][1])

    return resultPol

'''
    @param G: is a diGraph
    @param dizPolarGar: the dictionary with key as node and value its polarization
    @return the list of color of graph with node position
'''

def nodeColorGar(G,dizPolarGar,dizMerge):
    list=[]
    for i in G.nodes():
    #for i in dizMerge:
        if dizPolarGar.has_key(i):
            x= dizPolarGar[i][i][0]
            if x > 0. :
                list.append("blue")
            elif x < 0. :
                list.append("red")
            else:
                list.append("grey")
        else:
            print "Error"

    return list

'''
    @param G: is a diGraph
    @param dizPolarGar: the dictionary with key as node and value its polarization
    @return the dictionary of label of graph with node as key and value its polarization
'''
def nodeLaberGar(G,dizPolarGar):
    pol={}

    for i in G.nodes():
        if  dizPolarGar.has_key(i):
            #pol[i] = dizPolarGar[i][i][0]
            if dizPolarGar[i][i][0] == 0.0 or dizPolarGar[i][i][0] == 1.0 or dizPolarGar[i][i][0] == -1.0 :
                pol[i] = dizPolarGar[i][i][0]
            else:
                 pol[i]= "{0:.2f}".format(round(dizPolarGar[i][i][0],2))

        else:
            print "Error"


    return pol


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z





def main():
    # Leggo il file pickle dei retweet
    # Costruisco un grafo con networkx partendo dai dati ottenuti


    with open('../TweetOldSerialization/pickle/ElezioniSiciliaGraph/5Novembre/retweetListBlue.pkl','rb') as input:
     retweetListBlue = pickle.load(input)

    with open('../TweetOldSerialization/pickle/ElezioniSiciliaGraph/5Novembre/retweetListRed.pkl','rb') as input:
     retweetListRed = pickle.load(input)

    with open('../TweetOldSerialization/pickle/ElezioniSiciliaGraph/5Novembre/retweetListYellow.pkl','rb') as input:
     retweetListYellow = pickle.load(input)

    with open('../TweetOldSerialization/pickle/ElezioniSiciliaGraph/5Novembre/probRetBlue.pkl','rb') as input:
     probRetBlue = pickle.load(input)

    with open('../TweetOldSerialization/pickle/ElezioniSiciliaGraph/5Novembre/probRetRed.pkl','rb') as input:
     probRetRed = pickle.load(input)



    print "Fine Delete"
    List=[]
    for i in retweetListBlue:

        List.append(i)
    for i in retweetListRed:

        List.append(i)




    DizPesi={}

    for i in  probRetBlue:

          if not DizPesi.has_key(i):
              DizPesi[i]= probRetBlue[i]
          else:
              continue

    for i in probRetRed:

         if not DizPesi.has_key(i):
          DizPesi[i] = probRetRed[i]
         else:
            continue


    nodi_Blue= NodeDict(retweetListBlue)
    nodi_Red = NodeDict(retweetListRed)

    DizionarioPesiArchi={}

    G = createDirectNoWeightGraph(List)
    size_node_degree= []

    NumberRetweetDiz = getAllWeightEdge(DizPesi)
    #print NumberRetweetDiz
    UpdateNode(retweetListYellow,nodi_Blue)
    UpdateNode(retweetListYellow,nodi_Red)

    NodeDictDel(nodi_Blue,nodi_Red)


    setWeightEdge(G, NumberRetweetDiz, DizPesi)


    posizioneBlue = PosNode(G.nodes(),nodi_Blue)
    posizioneRed = PosNode(G.nodes(),nodi_Red)
    dizPosizioneBlue=PosNodeDizionario(G.nodes,nodi_Blue)
    dizPosizioneRed=PosNodeDizionario(G.nodes,nodi_Red)

    dizMerge = merge_two_dicts(dizPosizioneBlue, dizPosizioneRed)


    pos = nx.spring_layout(G)

    print(len(G.nodes()))
    edgeWeightLabel = nx.get_edge_attributes(G, 'weight')
    print("pesi archi",edgeWeightLabel)

    dictTest={}

    for i in G.nodes():
        if not dictTest.has_key(i):
            dictTest[i]= getProbRandomNeighbour(G,i,edgeWeightLabel)

    print("dictgetProbRandom",dictTest)


    result={}
    nodo=0
    for i in G.nodes():

            dictDegreeDiscRed = dictDegreeDiscendent(G,i,nodi_Red)
            dictDegreeDiscBlue = dictDegreeDiscendent(G,i,nodi_Blue)

            print nodo
            result[i]= performRandomWalkSingleNode(G,i,dictDegreeDiscBlue,dictDegreeDiscRed,int(math.sqrt(len(G.nodes()))),nodi_Red,"",dictTest,edgeWeightLabel)
            nodo = nodo +1



    print result,len(result)

    listColorGar = nodeColorGar(G,result,dizMerge)
    dictLabelGar={}
    dictLabelGar = nodeLaberGar(G,result)
    print(dictLabelGar)


    nx.write_gpickle(G, '../Test/Sicilia/5Novembre/grafoSicilia5Novembre.pickle', protocol=pickle.HIGHEST_PROTOCOL)
    with open('../Test/Sicilia/5Novembre/dizionarioPolarizzazioneRandomWalk.pickle',"wb") as output:
        pickle.dump(dictLabelGar,output,pickle.HIGHEST_PROTOCOL)
    with open('../Test/Sicilia/5Novembre/listaColoriPolarizzazioneRandomWalk.pickle',"wb") as output:
        pickle.dump(listColorGar,output,pickle.HIGHEST_PROTOCOL)

    nx.draw_networkx_nodes(G, pos, G.nodes(),node_size=150 ,with_labels=True , node_color=listColorGar)

    nx.draw_networkx_edges(G, pos, edge_color='g')

    nx.draw_networkx_labels(G, pos, dictLabelGar, font_size=8)
    #nx.draw_networkx_labels(G, pos, font_size=8)



    plt.savefig("../Test/Sicilia/5Novembre/Polarizzazione.png", format="PNG")

    plt.show()




if __name__ == '__main__':
    main()