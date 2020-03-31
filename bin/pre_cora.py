import random
import sys
sys.path.append('../')
import numpy as np
import torch
from dgl import DGLGraph

from core.data.constants import GRAPH, LABELS, TRAIN_MASK, TEST_MASK, VAL_MASK, N_CLASSES
from core.data.utils import complete_path, load_pickle, save_pickle
from core.models.constants import GNN_EDGE_LABELS_KEY
from core.models.constants import GNN_NODE_ATTS_KEY
from entropy.utils import read_adjMatrix_csv


def save_cora(out_folder):

    #label
    labels = []
    node_label_file = open('../bin/preprocessed_data/cora/node_labels.txt', "r").readlines()
    for line in node_label_file:
         labels.append(int(line))
    nodN = len(labels)
    labels=torch.from_numpy(np.array(labels))

    #mask
    random_idx=[i for i in range(nodN)]
    random.shuffle(random_idx)
    train_idx=random_idx[nodN//5:]
    test_idx=random_idx[:nodN//5]

    def _idx_to_mask(idx, n):
        mask = np.zeros(n, dtype=int)
        mask[idx] = 1
        return torch.ByteTensor(mask)

    val_idx = train_idx[:len(train_idx) // 5]
    val_mask = _idx_to_mask(val_idx, labels.shape[0])

    train_idx = train_idx[len(train_idx) // 5:]
    train_mask = _idx_to_mask(train_idx, labels.shape[0])

    test_mask = _idx_to_mask(test_idx, labels.shape[0])


    #node
    node_feature = []
    node_feature_file = open('../bin/preprocessed_data/cora/node_feature.txt', "r").readlines()
    for line in node_feature_file:
        vector = [float(x) for x in line.strip('\n').strip(',').split(",")]
        node_feature.append(vector)
    g = DGLGraph()
    g.add_nodes(nodN)
    g.ndata[GNN_NODE_ATTS_KEY] = torch.from_numpy(np.array(node_feature))


    #edge
    edge_entropy=[]
    edge_entropy_file=open('../bin/preprocessed_data/cora/edge_entropy.txt',"r").readlines()
    for line in edge_entropy_file:
        vector2 = [float(x) for x in line.strip('\n').strip(',').split(",")]
        edge_entropy.append(vector2)
    edge_entropy=torch.from_numpy(np.array(edge_entropy))

    attention_sum=torch.zeros(nodN,nodN)
    for i in range(8):
        attention=[]
        filename='../bin/preprocessed_data/cora/attentions/attention_{}.txt'.format(i)
        attention_file=open(filename,"r").readlines()
        for line in attention_file:
            vector3 = [float(x) for x in line.strip('\n').strip(',').split(",")]
            attention.append(vector3)
        attention=torch.from_numpy(np.array(attention))
        attention_sum=torch.add(attention_sum.double(),attention.double())

    attention_average=attention_sum*(1/8).unsqueeze(-1).expand(nodN,nodN,8) # 2708*2708*8

    edge_feature=torch.mul(attention_average,edge_entropy)

    g.edata[GNN_EDGE_LABELS_KEY] =edge_feature
    adj, N = read_adjMatrix_csv('./preprocessed_data/cora/adj.csv')
    for i in range(N):
        for j in range(N):
            if adj[i][j] > 0:
                g.add_edges(i, j)


    #save
    save_pickle(g, complete_path(out_folder, GRAPH))
    save_pickle(7, complete_path(out_folder, N_CLASSES))
    torch.save(labels, complete_path(out_folder, LABELS))
    torch.save(train_mask, complete_path(out_folder, TRAIN_MASK))
    torch.save(test_mask, complete_path(out_folder, TEST_MASK))
    torch.save(val_mask, complete_path(out_folder, VAL_MASK))

def load_cora(folder):
    data = {
        GRAPH: load_pickle(complete_path(folder, GRAPH)),
        #N_RELS: load_pickle(complete_path(folder, N_RELS)),
        N_CLASSES: load_pickle(complete_path(folder, N_CLASSES))
    }

    for k in [LABELS, TRAIN_MASK, TEST_MASK, VAL_MASK]:
        data[k] = torch.load(complete_path(folder, k))

    return data
