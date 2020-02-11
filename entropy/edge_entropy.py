import numpy as np

def edgeEntropy(entropyVactor,lines):
    #count_edge_file = "./data2/count_edge.csv"
    # f2 = open(entropyfilename, "r").readlines()
    # for line in f2:
    #     vector = [float(x) for x in line.split(",")]
    # print(vector)
    vector=entropyVactor
    number_vector = [1, 2, 3, 3, 3, 4, 4, 4]
    #
    # f = open(count_edge_file, "r")
    # lines = f.readlines()
    Node = len(lines)

    edge_entropy_matrix = np.zeros((Node, Node), np.float)
    line_number = 0
    for line in lines:
        column_number = 0
        for edge_motif in line:

            if edge_motif == '0':
                column_number += 1
            else:
                edge_entropy = 0
                for motif_number in edge_motif:
                    if motif_number != '0':
                        motif_num = int(motif_number)
                        index = motif_num - 1
                        edge_entropy += vector[index] / number_vector[index]
                edge_entropy_matrix[line_number][column_number] = edge_entropy
                edge_entropy_matrix[column_number][line_number] = edge_entropy
        line_number += 1

    #np.savetxt("./data2/edge_entropy.csv", edge_entropy_matrix, delimiter=",", fmt="%f")
    return edge_entropy_matrix