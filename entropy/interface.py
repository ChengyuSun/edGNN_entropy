from entropy.CountMotif_nr import countMotifs
from entropy.Entropy import graphEntropy
from entropy.edge_entropy import edgeEntropy
from entropy.countedge import countEdge
import entropy.io as io
import numpy as np


def writeEdgeEntropy(graphfile):
    if graphfile.endswith(".xlsx"):
        graphfile=io.translata_xlsx_to_csv(graphfile)
        print('转变格式成功')
    A, nodN = io.read_adjMatrix_csv(graphfile)
    return edgeEntropy(graphEntropy(countMotifs(A,nodN)),countEdge(A,nodN))

writeEdgeEntropy('./data/graph10.xlsx')


def writeEdgeAttribute(graph_ids,adj):
    edge_entropys=[]
    # build graphs with nodes
    edge_index=0
    for g_id in graph_ids:
        node_ids = np.argwhere(graph_ids == g_id).squeeze()
        node_ids.sort()

        temp_nodN=len(node_ids)
        temp_A=np.zeros([temp_nodN,temp_nodN],int)

        edge_index_begin=edge_index

        while adj[edge_index][0] in node_ids:
            temp_A[adj[edge_index][0]][adj[edge_index][1]]=1
            edge_index+=1

        entropy_matrix = edgeEntropy(graphEntropy(countMotifs(temp_A, temp_nodN)),countEdge(temp_A, temp_nodN))

        for j in (edge_index_begin,edge_index):
            edge_entropys[j]=entropy_matrix[adj[j][0]][adj[j][1]]

    return edge_entropys