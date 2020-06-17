import sys
sys.path.append('../')

import numpy as np

import entropy.utils as utils
from entropy.CountMotif_nr import countMotifs
from entropy.Entropy import graphEntropy
from entropy.countedge import countEdge
from entropy.edge_entropy import edgeEntropy
from bin.pre_pub import read_label,read_adj


def writeEdgeEntropy(graphfile):
    if graphfile.endswith(".xlsx"):
        graphfile=utils.translata_xlsx_to_csv(graphfile)
        print('转变格式成功')
    A, nodN = utils.read_adjMatrix_csv(graphfile)
    count_edge,count_motif=countEdge(A,nodN)
    print('count_motif:',count_motif)
    graph_entropy=graphEntropy(count_motif,nodN)
    print('graph_entropy:',graph_entropy)
    edge_entropy=edgeEntropy(graph_entropy,count_edge,count_motif)
    return edge_entropy

def read_txt():
    array = open('../bin/preprocessed_data/citeseer/citeseer/citeseer_adj.txt').readlines()
    N = len(array)
    matrix = []
    for line in array:
        line = line.strip('\n').strip(',').split(',')
        line = [int(x) for x in line]
        matrix.append(line)
    matrix = np.array(matrix)
    return matrix,len(matrix)


def _entropy():
    nodN,labels=read_label()
    A,_=read_adj(nodN)
    count_edge=[]
    count_edge_file= open('../bin/preprocessed_data/pub/pub_count_edge.txt', "r").readlines()
    for line in count_edge_file:
        vector = [str(x) for x in line.strip('\n').strip(',').split(",")]
        count_edge.append(vector)
    print(count_edge[0])
    print('count_edge.len: ',len(count_edge))
    print('count_edge[0].len: ',len(count_edge[0]))
    return
    count_motif=[3643, 2726, 12520, 1148, 2015, 54312, 896, 1776]
    graph_entropy = graphEntropy(count_motif, nodN)
    print('graph_entropy:', graph_entropy)
    edge_entropy = edgeEntropy(graph_entropy, count_edge, count_motif)
    return edge_entropy

_entropy()


def edgeEntropy_node_class(edge_src,edge_dst,nodN):
    edgeN=len(edge_src)
    A=np.zeros([nodN,nodN],int)
    for i in range(edgeN):
        A[edge_src[i]][edge_dst[i]]=1
    for i in range(nodN):
        A[i][i]=0
    entropy_matrix=edgeEntropy(graphEntropy(countMotifs(A, nodN), nodN), countEdge(A,nodN))
    edge_entropys=[]
    for i in range(edgeN):
        edge_entropys.append(entropy_matrix[edge_src[i]][edge_dst[i]])
    return edge_entropys

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