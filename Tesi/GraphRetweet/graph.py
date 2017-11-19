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

    def __init__(self,user, retweet):

        self.user = user
        self.retweet = retweet



def createGraph(retweetList):
    G = nx.Graph()
    for i in range(0,len(retweetList)):
        print ("pos" + str(i)+"username="+ retweetList[i].user +"ret="+str(retweetList[i].retweet))
        if( retweetList[i].retweet == "" ):
            G.add_nodes_from(retweetList[i].user,color='green')

        else:
            for j in range(0,len(retweetList[i].retweet)):
                G.add_edge(retweetList[i].user,retweetList[i].retweet[j])

    return G


def main():
    # Leggo il file pickle dei retweet
    # Costruisco un grafo con networkx partendo dai dati ottenuti
    with open('/home/alessandro/PycharmProjects/Tesi/TweetOldSerialization/pickle/retweet_data.pkl', 'rb') as input:
        retweetList = pickle.load(input)
        G = createGraph(retweetList)
        size_node_degree= []

    for nodes in G.nodes():
       # print ("Grado nodo = "+str(nodes))
        if(G.degree(nodes) == 0):
            size_node_degree.append(0.5)
        else:
            size_node_degree.append(1/G.degree(nodes))

    for i in range(0,len(size_node_degree)):
        print(size_node_degree[i])

    partition = community.best_partition(G)

    size = float(len(set(partition.values())))

    pos = nx.spring_layout(G)
    count = 0.
    #cambio i colori dei nodi a seconda del loro grado
    node_color = []
    for node in G:
        print node
        if G.degree(node) > 10:
            node_color.append('yellow')
        else:
            node_color.append('red')
   #cambio l size dei nodi in basi al grado del nodo
    size_node=[]
    for node in G:
        if G.degree(node) > 10:
            size_node.append(30)
        elif G.degree(node) >5 & G.degree(node) <= 10:
            size_node.append(8)
        elif G.degree(node) >1 & G.degree(node) <= 5:
            size_node.append(6)
        else:
            size_node.append(4)


   # nx.draw(G,pos,nodelist=G.nodes,node_size=20, node_color=node_color, with_labels=True)

    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos ,list_nodes, node_size=size_node, node_color= node_color)

    nx.draw_networkx_edges(G, pos, alpha=0.5,edge_color='b')

    #nx.draw_networkx_labels(G, pos, int=size_node)

    plt.show()

if __name__ == '__main__':
    main()