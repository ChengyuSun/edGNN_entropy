import numpy as np


def edgeEntropy(graph_entropy,countEdges,countmotifs):
    number_vector = [1, 2, 3, 3, 3, 4, 4, 4]
    Node = len(countEdges)
    edge_entropy_matrix = np.zeros((Node, Node,8), np.float)
    line_number = 0

    print('start calculationg edge-entropys')
    for line in countEdges:
        column_number = 0
        for edge_motif in line:
            if edge_motif == '0':
                column_number += 1
                continue
            else:
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
        print('正在计算边熵行数为： ', line_number)
    with open('/new_disk_B/scy/pub/pub_edge_entropy.txt', 'w') as file:
        for i in range(Node):
            for j in range(Node):
                for k in edge_entropy_matrix[i][j]:
                    file.write(str(k)+',')
                file.write('\n')
    return edge_entropy_matrix