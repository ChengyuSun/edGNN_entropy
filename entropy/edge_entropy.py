import numpy as np


entropy_vector_file = "./../data/E_256_mutag.csv"
count_edge_file = "./../data/count_edge_mutag.csv"
edge_entropy_file ="./../data/edge_entropy_mutag.csv"

f2 = open(entropy_vector_file, "r").readlines()
for line in f2:
    vector = [float(x) for x in line.split(",")]
print(vector)
number_vector = [1,2,3,3,3,4,4,4]


f = open(count_edge_file, "r")
lines = f.readlines()
Node = len(lines)

edge_entropy_matrix = np.zeros((Node, Node), np.float)
line_number = 0
for line in lines:
    line = line.strip('\n').split(',')
    column_number = 0
    for edge_motif in line:

        if edge_motif == '0':
            column_number +=1
        else:
            edge_entropy =0
            for motif_number in edge_motif:
                if motif_number !='0':
                    motif_num = int(motif_number)
                    index = motif_num-1
                    edge_entropy += vector[index]/number_vector[index]
            edge_entropy_matrix[line_number][column_number] = edge_entropy
            edge_entropy_matrix[column_number][line_number] = edge_entropy
    line_number += 1

np.savetxt(edge_entropy_file, edge_entropy_matrix, delimiter=",", fmt="%f")
