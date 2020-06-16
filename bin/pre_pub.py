import numpy as np
import torch


def read_label():
    label_dir=dict()
    labels=[]
    #../bin/preprocessed_data/pub/pub_label.txt
    node_label_file = open('D:/1科研/data/pub/pub_label.txt', "r").readlines()
    for line in node_label_file:
        vector = [float(x) for x in line.strip('\n').split(" : ")]
        label_dir[vector[0]]=vector[1]
    nodN = label_dir.__len__()
    for i in range(nodN):
        labels.append(label_dir[i])
    labels = torch.from_numpy(np.array(labels))
    print(labels.shape())
    return labels

read_label()

def read_adj():
    adj_file = open('../bin/preprocessed_data/pub/pub_adj.txt', "r").readlines()
    for line in adj_file:
        return