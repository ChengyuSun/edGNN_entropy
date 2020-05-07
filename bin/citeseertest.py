import numpy as np

node_name_to_index = dict()
node_index_to_att = dict()
node_index_to_class = dict()
label_to_class = dict()
index = 0
class_label = 0
content_file = open('./citeseer.content', "r").readlines()
for line in content_file:
    vector = [x for x in line.strip('\n').split('\t')]
    if not label_to_class.__contains__(vector[3704]):
        label_to_class[vector[3704]] = class_label
        class_label += 1
    node_name_to_index[vector[0]] = index
    node_index_to_att[index] = vector[1:3704]
    node_index_to_class[index] = label_to_class[vector[3704]]
    index += 1

nodN = len(node_name_to_index)
dim = len(node_index_to_att[0])

edge_num=0
adj = np.zeros((nodN, nodN))
cite_file = open('./citeseer.cites', "r").readlines()
for line in cite_file:
    vector = [x for x in line.strip('\n').split('\t')]
    if not node_name_to_index.__contains__(vector[0]) \
            or not node_name_to_index.__contains__(vector[1])\
            or vector[0]==vector[1]:
        continue

    start = node_name_to_index[vector[0]]
    end = node_name_to_index[vector[1]]
    # if start==end:
    #   print(str(vector[0])+'->'+str(vector[1]))
    # #print(str(start) + '->' + str(end))
    adj[start][end] = 1
    adj[end][start] = 1
    edge_num+=2

print('edge_num:',edge_num)



with open('./citeseer_adj.txt', 'w') as adj_file:
    for i in range(nodN):
        for j in range(nodN):
            adj_file.write(str(adj[i][j]) + ',')
        adj_file.write('\n')

with open('./node_features.txt', 'w') as feature_file:
    for i in range(nodN):
        for j in range(dim):
            feature_file.write(node_index_to_att[i][j] + ',')
        feature_file.write('\n')

with open('./node_labels.txt', 'w') as label_file:
    for i in range(nodN):
        label_file.write(str(node_index_to_class[i]) + '\n')


