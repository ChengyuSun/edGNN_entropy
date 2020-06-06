import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from core.data.utils import complete_path

GRAPH_LABELS_SUFFIX = '_graph_labels.txt'
NODE_LABELS_SUFFIX = '_node_labels.txt'
ADJACENCY_SUFFIX = '_A.txt'
GRAPH_ID_SUFFIX = '_graph_indicator.txt'

def ana():
    data = dict()
    dataset_name='MUTAG'
    dirpath = './preprocessed_data/{}/unzipped/{}'.format(dataset_name,dataset_name)
    for f in os.listdir(dirpath):
        if "README" in f or '.txt' not in f:
            continue
        fpath = complete_path(dirpath, f)
        suffix = f.replace(dataset_name, '')
        print(suffix)
        if 'attributes' in suffix:
            data[suffix] = np.loadtxt(fpath, dtype=np.float, delimiter=',')
        else:
            data[suffix] = np.loadtxt(fpath,dtype=np.int, delimiter=',')

    graph_ids = set(data['_graph_indicator.txt'])

    node_label_num=max(data[NODE_LABELS_SUFFIX])-min(data[NODE_LABELS_SUFFIX])+1
    print('node labels number: ',node_label_num)

    adj=data[ADJACENCY_SUFFIX]
    edge_index=0
    node_index_begin = 0
    b=0
    for g_id in set(graph_ids):
        print('正在处理图：'+str(g_id))
        node_ids = np.argwhere(data['_graph_indicator.txt'] == g_id).squeeze()
        node_ids.sort()

        temp_nodN=len(node_ids)
        temp_A=np.zeros([temp_nodN,temp_nodN],int)
        print('nodN: ',temp_nodN)
        while (edge_index<len(adj))and(adj[edge_index][0]-1 in node_ids):
            temp_A[adj[edge_index][0]-1-node_index_begin][adj[edge_index][1]-1-node_index_begin]=1
            edge_index+=1

        print(temp_A)

        node_labels=data[NODE_LABELS_SUFFIX][node_ids]

        draw_graph(temp_A,node_labels,temp_nodN,data[GRAPH_LABELS_SUFFIX][g_id])

        node_index_begin += temp_nodN

        b+=1
        if b>10:
            break


def draw_graph(adj,node_labels,nodN,label):
    colors=['red','blue','green','orange','gray','pink','yellow']
    G = nx.Graph()
    G.add_nodes_from([i for i in range(nodN)])
    for j in range(nodN):
        for k in range(nodN):
            if adj[j][k]>0:
                G.add_edge(j,k)

    color_map = []
    for node in G:
        color_map.append(colors[node_labels[node]])

    plt.title(str(label), fontsize=20)
    nx.draw(G, node_color=color_map, with_labels=True,pos=nx.spring_layout(G))

    plt.show()
    return


def count_perssad(adj,node_labels,nodN):


    return

ana()