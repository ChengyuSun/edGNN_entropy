import numpy as np

import entropy.utils as utils
from entropy.CountMotif_nr import countMotifs
from entropy.Entropy import graphEntropy
from entropy.countedge import countEdge
from entropy.edge_entropy import edgeEntropy


def writeEdgeEntropy(graphfile):
    if graphfile.endswith(".xlsx"):
        graphfile=utils.translata_xlsx_to_csv(graphfile)
        print('转变格式成功')
    A, nodN = utils.read_adjMatrix_csv(graphfile)
    print('A\n'+str(A))
    temp=countEdge(A,nodN)
    print('count_edge\n'+str(temp))
    return edgeEntropy(graphEntropy(countMotifs(A,nodN),nodN),temp)
    #return countEdge(A,nodN)

#print(writeEdgeEntropy('./data/graph11.xlsx'))

def writeEdgeAttribute(graph_ids,adj):
    edge_entropys=[]
    # build graphs with nodes
    edge_index=0
    node_index_begin=0
    for g_id in set(graph_ids):
        print('正在处理图：'+str(g_id))
        node_ids = np.argwhere(graph_ids == g_id).squeeze()
        node_ids.sort()

        temp_nodN=len(node_ids)
        temp_A=np.zeros([temp_nodN,temp_nodN],int)

        edge_index_begin=edge_index

        while (edge_index<len(adj))and(adj[edge_index][0]-1 in node_ids):
            temp_A[adj[edge_index][0]-1-node_index_begin][adj[edge_index][1]-1-node_index_begin]=1
            edge_index+=1

        entropy_matrix = edgeEntropy(graphEntropy(countMotifs(temp_A, temp_nodN),temp_nodN),countEdge(temp_A, temp_nodN))

        #print(str(edge_index_begin)+'  加入属性的起止边：'+str(edge_index-1))
        for j in range(edge_index_begin,edge_index):
            edge_entropys.append(entropy_matrix[adj[j][0]-1-node_index_begin][adj[j][1]-1-node_index_begin])

        node_index_begin+=temp_nodN
    return edge_entropys