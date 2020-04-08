import numpy as np

from entropy.utils import read_adjMatrix_csv


def edgeEntropy(graph_entropy,countEdges,countmotifs):
    number_vector = [1, 2, 3, 3, 3, 4, 4, 4]
    Node = len(countEdges)
    edge_entropy_matrix = np.zeros((Node, Node,8), np.float)
    line_number = 0

    adj, N = read_adjMatrix_csv('../bin/preprocessed_data/cora/adj.csv')
    print('start calculationg edge-entropys')

    for line in countEdges:
        column_number = 0

        for edge_motif in line:
            if (adj[line_number][column_number] != adj[column_number][line_number]):
                print('adj error in {} {}'.format(line_number, column_number))

            if edge_motif == '0':

                if (adj[line_number][column_number] != 0):
                    print('edge  {},{}  has no entropy'.format(line_number, column_number))

                column_number += 1
                continue
            else:

                if (adj[line_number][column_number]==0):
                    print('error in {},{}'.format(line_number, column_number))

                edge_entropy = [0 for i in range(8)]
                for motif_number in edge_motif:
                    if motif_number != '0':
                        motif_num = int(motif_number)
                        index = motif_num - 1
                        edge_entropy[index] += graph_entropy[index] / (countmotifs[index]*number_vector[index])
                edge_entropy_matrix[line_number][column_number] = edge_entropy
                edge_entropy_matrix[column_number][line_number] = edge_entropy
                column_number += 1
        line_number += 1
        print('line',line_number)

    return edge_entropy_matrix

    with open('../entropy/data/edge_entropy.txt', 'w') as file:
        for i in range(Node):
            for j in range(Node):
                for k in edge_entropy_matrix[i][j]:
                    file.write(str(k)+',')
                file.write('\n')
    return edge_entropy_matrix