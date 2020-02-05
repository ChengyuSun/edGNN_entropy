from entropy.CountMotif_nr import countMotifs
from entropy.Entropy import graphEntropy
from entropy.edge_entropy import edgeEntropy
from entropy.countedge import countEdge
import entropy.io as io

def writeEdgeEntropy(graphfile):
    if graphfile.endswith(".xlsx"):
        graphfile=io.translata_xlsx_to_csv(graphfile)
        print('转变格式成功')
    A, nodN = io.read_adjMatrix_csv(graphfile)
    countEdge(A,nodN)
    edgeEntropy(graphEntropy(countMotifs(A,nodN)))

#先把图中的边找出，建立完整的邻接矩阵，
# 然后算出边熵矩阵，最后稀疏化成边属性，返回
def edgeEntropy(graph):
    return