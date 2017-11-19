import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np
import string
import  community




G = nx.Graph()

with open('test2.csv') as myFile:
    reader = csv.reader(myFile)
    lista_righe = []
    for row in reader:
       # print(row[0])
        match = False
        lista_righe.append(row)
        for row2 in lista_righe:
           #  print(row2[1]+"=="+row[1])
             if(row2[1] == row[1]):
               # print('trovato'+row2[1])
                G.add_edge(row[0],row2[0],edges=row[1])
                match = True

        if(match == False):
            G.add_node(row[0],autore=row[0])

pos=nx.spring_layout(G)
d = nx.degree(G)

d= [(d[node]+1) for node in G.nodes()]

print(len(G.edges))
lista_colori= []
lista_colori.append(np.linspace(0,1,len(G.edges())))
# nx.draw(G,pos,node_color = np.linspace(0,1,len(G.nodes())),
#        # edge_color = lista_colori,
#         width = 3.0,
#         with_labels=True
#        # labels = {n:l for n,l in zip(G.nodes(),string.ascii_uppercase)}
#         )
#nx.draw_networkx_edge_labels(G,pos,nodelist=d ,node_size=[(v+1)*100 for v in d],with_labels=True, font_weight='bold')
#plt.subplot(122)
#nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
#plt.show()

#first compute the best partition
partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
label_node=[]
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    label_node = [nodes for nodes in G.nodes()]
   # print(label_node)
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,alfa=0 ,
                                node_color = str(np.linspace(0,1,len(list_nodes))))


nx.draw_networkx_edges(G,pos, alpha=0.5, edge_color=str(float(len(set(G.nodes())))/float(len(set(G.edges())))))
nx.draw_networkx_labels(G,pos,int=12,font_color='r',alfa=0)
plt.show()



