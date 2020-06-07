import sys
sys.path.append('../')
import numpy as np
import torch
from dgl import DGLGraph
import os

from core.data.constants import GRAPH, LABELS, N_CLASSES
from core.data.utils import complete_path, save_pickle
from core.models.constants import GNN_NODE_ATTS_KEY,GNN_EDGE_FEAT_KEY
from entropy.utils import read_adjMatrix_txt


def save_cora(out_folder):

    #label
    labels = []

    #''
    #node_label_file = open('../bin/preprocessed_data/cora/node_labels.txt', "r").readlines()
    node_label_file = open('../bin/preprocessed_data/citeseer/citeseer/node_labels.txt', "r").readlines()
    for line in node_label_file:
         labels.append(int(line))
    nodN = len(labels)
    label_num=max(labels)-min(labels)+1
    labels=torch.from_numpy(np.array(labels))

    #node
    node_feature = []
    #node_feature_file = open('../bin/preprocessed_data/cora/node_feature.txt', "r").readlines()
    node_feature_file = open('../bin/preprocessed_data/citeseer/citeseer/node_features.txt', "r").readlines()
    for line in node_feature_file:
        vector = [float(x) for x in line.strip('\n').strip(',').split(",")]
        node_feature.append(vector)
    g = DGLGraph()
    g.add_nodes(nodN)
    g.ndata[GNN_NODE_ATTS_KEY] = torch.from_numpy(np.array(node_feature))
    print('g.ndata[GNN_NODE_ATTS_KEY]:',g.ndata[GNN_NODE_ATTS_KEY].size())

    #edge
    edge_entropy=[]
    #edge_entropy_file=open('../bin/preprocessed_data/cora/edge_entropy.txt',"r").readlines()
    edge_entropy_file = open('../bin/preprocessed_data/citeseer/citeseer/citeseer_edge_entropy.txt', "r").readlines()
    for line in edge_entropy_file:
        vector2 = [float(x) for x in line.strip('\n').strip(',').split(",")]
        # sum=0
        # for item in vector2:
        #     sum+=item
        # edge_entropy.append(sum)
        edge_entropy.append(vector2)

    edge_entropy=torch.from_numpy(np.array(edge_entropy)).view(nodN*nodN,8)
    print('edge_entropy:',edge_entropy.size())

    edge_feature_all = edge_entropy.numpy()
    edge_feature=[]
    adj, N = read_adjMatrix_txt('../bin/preprocessed_data/citeseer/citeseer/citeseer_adj.txt')
    #adj,N=read_adjMatrix_csv('../bin/preprocessed_data/cora/adj.csv')
    for i in range(N):
        for j in range(N):
            if adj[i][j] > 0:
                g.add_edges(i, j)
                edge_feature.append(edge_feature_all[i*N+j])


    g.edata[GNN_EDGE_FEAT_KEY] = torch.from_numpy(edge_feature)
    print('g.edata[GNN_EDGE_FEAT_KEY]',g.edata[GNN_EDGE_FEAT_KEY].size())


    #save
    if  not os.path.exists(out_folder):
        os.makedirs(out_folder)
    save_pickle(g, complete_path(out_folder, GRAPH))
    save_pickle(label_num, complete_path(out_folder, N_CLASSES))
    torch.save(labels, complete_path(out_folder, LABELS))
    # torch.save(train_mask, complete_path(out_folder, TRAIN_MASK))
    # torch.save(test_mask, complete_path(out_folder, TEST_MASK))
    # torch.save(val_mask, complete_path(out_folder, VAL_MASK))



