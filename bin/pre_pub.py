import numpy as np
import torch


def read_label_pub():
    label_dir=dict()
    labels=[]
    node_label_file = open('/new_disk_B/scy/pub/pub_label.txt', "r").readlines()
    for line in node_label_file:
        vector = [int(x) for x in line.strip('\n').split(" : ")]
        label_dir[vector[0]]=vector[1]
    nodN = label_dir.__len__()
    for i in range(nodN):
        labels.append(label_dir[i])
    label_num = max(labels) - min(labels) + 1
    labels = torch.from_numpy(np.array(labels))
    return  labels,nodN,label_num

def read_adj_pub(nodN):
    adj=np.zeros((nodN,nodN),int)
    adj_file = open('/new_disk_B/scy/pub/pub_adj.txt', "r").readlines()
    counter=0
    for line in adj_file:
        vector = [int(x) for x in line.strip('\n').split(" ")]
        adj[vector[0]][vector[1]]=1
        adj[vector[1]][vector[0]] = 1
        counter+=1
    for i in range(nodN):
        if adj[i][i]==1:
            adj[i][i]=0
    return adj,nodN

def read_feature_pub():
    feature_file = open('/new_disk_B/scy/pub/pub_feature.txt', "r").readlines()
    features=[]
    for line in feature_file:
        if line=='\n':
            continue
        vector = [float(x) for x in line.strip('\n').strip(' ').split(" ")]
        if len(vector)!=500:
            print(len(vector))
        features.append(vector)
    return features
