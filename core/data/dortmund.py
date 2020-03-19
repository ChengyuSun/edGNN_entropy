import os
import zipfile

import numpy as np
import torch
from dgl import DGLGraph

import core.data.utils as utils
from core.data.constants import GRAPH, LABELS, N_CLASSES, N_ENTITIES
from core.data.utils import complete_path
from core.models.constants import GNN_EDGE_LABELS_KEY, GNN_EDGE_NORM
from core.models.constants import GNN_NODE_LABELS_KEY, GNN_NODE_ATTS_KEY, GNN_EDGE_FEAT_KEY

ADJACENCY_SUFFIX = '_A.txt'
GRAPH_ID_SUFFIX = '_graph_indicator.txt'
GRAPH_LABELS_SUFFIX = '_graph_labels.txt'
NODE_LABELS_SUFFIX = '_node_labels.txt'
# optional
EDGE_LABELS_SUFFIX = '_edge_labels.txt'
EDGE_ATT_SUFFIX = '_edge_attributes.txt'
NODE_ATT_SUFFIX = '_node_attributes.txt'
GRAPH_ATT_SUFFIX = '_graph_attributes.txt'

SUFFIX = [
    ADJACENCY_SUFFIX,
    GRAPH_ID_SUFFIX,
    GRAPH_LABELS_SUFFIX,
    NODE_LABELS_SUFFIX,
    EDGE_LABELS_SUFFIX,
    EDGE_ATT_SUFFIX,
    NODE_ATT_SUFFIX,
    GRAPH_ATT_SUFFIX
]

BASE_URL = 'https://ls11-www.cs.tu-dortmund.de/people/morris/graphkerneldatasets/'
EXTENSION = '.zip'


def check_suffix(fname):
    for suffix in SUFFIX:
        if fname.endswith(suffix):
            return SUFFIX
    return None


def preprocess_dortmund(*, dataset, out_folder):
    """
    Preprocessing function for datasets provided at https://ls11-www.cs.tu-dortmund.de/staff/morris/graphkerneldatasets

    Args:
      dataset (str): dataset name (from ptc_fm, ptc_fr, ptc_mm, ptc_mr)
      out_folder (str): path to folder where to save preprocessed graph
    """
    DATASET_PATH = complete_path(out_folder, dataset + '.zip')
    #
    # dataset_url = "".join([BASE_URL, dataset.upper(), EXTENSION])
    # r = requests.get(dataset_url, allow_redirects=True)
    # r.raise_for_status()
    #
    # with open(DATASET_PATH, 'wb') as fhandle:
    #     fhandle.write(r.content)

    EXTRACT_FOLDER = complete_path(out_folder, 'unzipped')
    with zipfile.ZipFile(DATASET_PATH, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)

    d = os.listdir(EXTRACT_FOLDER)
    if len(d) != 1:
        raise RuntimeError
    dataset_name = d[0]
    dirpath = complete_path(EXTRACT_FOLDER, dataset_name)
    data = dict()
    fpath = ''
    for f in os.listdir(dirpath):
        if f.startswith('README'):
            continue
        fpath = complete_path(dirpath, f)
        suffix = f.replace(dataset_name, '')
        if 'attributes' in suffix:
            data[suffix] = np.loadtxt(fpath, dtype=np.float, delimiter=',',
                                      encoding='utf-8')
        else:
            data[suffix] = np.loadtxt(fpath, dtype=np.int, delimiter=',',
                                      encoding='utf-8')

    graph_ids = set(data[GRAPH_ID_SUFFIX])
    node2graph = dict()
    graphs = dict()
    graph_labels = dict()

    node2node_per_graph = dict()

    # build graphs with nodes
    """
    graphs: map graph_id to a DGLGraph object
    graph_ids: distinct id for all graphs
    graph_labels: a dict maps graph_id to its label, which is a ndarray
    g_id: current graph id
    node_ids / n_id: global node ids from the dataset of the current graph
    node2graph: a dict maps n_id to graph_id(g_id)
    n2n: a dict maps n_id to relative position in the current graph
    """
    for g_id in graph_ids:
        node_ids = np.argwhere(data[GRAPH_ID_SUFFIX] == g_id).squeeze()
        node_ids.sort()
        n2n = dict()

        for idx, n_id in enumerate(node_ids):
            node2graph[n_id] = g_id
            n2n[n_id] = idx

        g = DGLGraph()

        g.add_nodes(len(node_ids), {GNN_NODE_LABELS_KEY: torch.from_numpy(data[NODE_LABELS_SUFFIX][node_ids])})
        if NODE_ATT_SUFFIX in data:
            g.ndata[GNN_NODE_ATTS_KEY] = torch.from_numpy(data[NODE_ATT_SUFFIX][node_ids])

        graphs[g_id] = g
        node2node_per_graph[g_id] = n2n
        graph_labels[g_id] = data[GRAPH_LABELS_SUFFIX][g_id - 1]

    # 边熵作为属性加入data中

    # data[EDGE_ATT_SUFFIX]=writeEdgeAttribute(data[GRAPH_ID_SUFFIX],data[ADJACENCY_SUFFIX])
    # np.savetxt(out_folder+'/edge_att.csv', data[EDGE_ATT_SUFFIX], delimiter="\n", fmt="%f")

    # process edges
    """
    orig_edge: an edge from the dataset
    n_id_0: start node of an edge
    """
    for i in range(len(data[ADJACENCY_SUFFIX])):
        orig_edge = data[ADJACENCY_SUFFIX][i] - 1

        n_id_0 = orig_edge[0]
        g_id = node2graph[n_id_0]
        n2n = node2node_per_graph[g_id]

        edata = {}

        if EDGE_LABELS_SUFFIX in data:
            edata[GNN_EDGE_LABELS_KEY] = torch.from_numpy(np.expand_dims(np.array(data[EDGE_LABELS_SUFFIX][i]), axis=0))

        if EDGE_ATT_SUFFIX in data:
            edata[GNN_EDGE_FEAT_KEY] = torch.from_numpy(np.expand_dims(np.array(data[EDGE_ATT_SUFFIX][i]), axis=0))

        graphs[g_id].add_edge(n2n[n_id_0], n2n[orig_edge[1]], edata)

    graph_list = []  # store all the GDLgraph objects
    labels = []      # store all label arrays

    for g_id in graphs.keys():
        graph_list.append(graphs[g_id])
        labels.append(graph_labels[g_id])

    # add edge normalization
    if EDGE_LABELS_SUFFIX in data:
        for graph in graph_list:                # graph: a GDLgraph object
            edge_src, edge_dst = graph.edges()  # two nodes of an edge
            edge_dst = list(edge_dst.data.numpy())
            edge_type = list(graph.edata[GNN_EDGE_LABELS_KEY])
            _, inverse_index, count = np.unique((edge_dst, edge_type), axis=1, return_inverse=True,
                                                return_counts=True)
            degrees = count[inverse_index]
            edge_norm = np.ones(len(edge_dst), dtype=np.float32) / degrees.astype(np.float32)
            graph.edata[GNN_EDGE_NORM] = torch.FloatTensor(edge_norm)

    label_set = set(labels)
    num_labels = len(label_set)
    mapping = dict(zip(label_set, list(range(num_labels))))
    labels = [mapping[label] for label in labels]

    num_entities = len(set(data[NODE_LABELS_SUFFIX]))

    if EDGE_LABELS_SUFFIX in data:
        num_rels = len(set(data[EDGE_LABELS_SUFFIX]))

    torch.save(torch.LongTensor(labels), complete_path(out_folder, LABELS))

    utils.save_pickle(num_labels, complete_path(out_folder, N_CLASSES))
    utils.save_pickle(num_entities, complete_path(out_folder, N_ENTITIES))
    # utils.save_pickle(num_rels, complete_path(out_folder, N_RELS))
    utils.save_pickle(graph_list, complete_path(out_folder, GRAPH))


def load_dortmund(folder):
    data = {
        GRAPH: utils.load_pickle(complete_path(folder, GRAPH)),
        N_CLASSES: utils.load_pickle(complete_path(folder, N_CLASSES)),
        N_ENTITIES: utils.load_pickle(complete_path(folder, N_ENTITIES)),
        # N_RELS: utils.load_pickle(complete_path(folder, N_RELS))
    }

    for k in [LABELS]:
        data[k] = torch.load(complete_path(folder, k))

    return data
