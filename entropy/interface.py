from entropy.CountMotif_nr import countMotifs
from entropy.Entropy import graphEntropy
from entropy.edge_entropy import edgeEntropy
from entropy.countedge import countEdge

def writeEdgeEntropy(graphfile_xlsx):
    countEdge(graphfile_xlsx)
    edgeEntropy(graphEntropy(countMotifs(graphfile_xlsx)))



