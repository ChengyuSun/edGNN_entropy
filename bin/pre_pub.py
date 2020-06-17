import numpy as np
import torch


def read_label():
    label_dir=dict()
    labels=[]
    node_label_file = open('../bin/preprocessed_data/pub/pub_label.txt', "r").readlines()
    for line in node_label_file:
        vector = [int(x) for x in line.strip('\n').split(" : ")]
        label_dir[vector[0]]=vector[1]
    nodN = label_dir.__len__()
    for i in range(nodN):
        labels.append(label_dir[i])
    labels = torch.from_numpy(np.array(labels))
    return  nodN,labels


def read_adj(nodN):
    adj=np.zeros((nodN,nodN),int)
    adj_file = open('../bin/preprocessed_data/pub/pub_adj.txt', "r").readlines()
    for line in adj_file:
        vector = [float(x) for x in line.strip('\n').split(" ")]
        adj[vector[0]][vector[1]]=1
        adj[vector[1]][vector[0]] = 1
    return adj,nodN