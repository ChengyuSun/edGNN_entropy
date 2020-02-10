from entropy.CountMotif_nr import countMotifs
from entropy.Entropy import graphEntropy
from entropy.edge_entropy import edgeEntropy
from entropy.countedge2 import countEdge
import entropy.io as io
import numpy as np




def writeEdgeEntropy(graphfile):
    if graphfile.endswith(".xlsx"):
        graphfile=io.translata_xlsx_to_csv(graphfile)
        print('转变格式成功')
    A, nodN = io.read_adjMatrix_csv(graphfile)
    print (nodN)
    print(graphEntropy(countMotifs(A,nodN)))
    #return edgeEntropy(graphEntropy(countMotifs(A,nodN)),countEdge(A,nodN))

writeEdgeEntropy('./data/graph10.xlsx')
#[1370.75412633478, 2031.57642082471, 2684.42807014950, 2343.47407192012, 2823.58794538322, 2712.47225114148, 2454.89736525705, 2865.86486071414]
#[1369.16883438083, 2029.99112887076, 2682.84277819555, 2341.88877996617, 2822.00265342927, 2710.88695918753, 2453.31207330310, 2864.27956876019]
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