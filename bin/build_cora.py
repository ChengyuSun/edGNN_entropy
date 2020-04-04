import sys
sys.path.append('../')
from pre_cora import save_cora
import argparse
from dgl.data import register_data_args

parser = argparse.ArgumentParser(description='build cora')
register_data_args(parser)
# parser.add_argument("--path", type=str, required=True,
#                         help="Path from where to save cora")
parser.add_argument("--label", type=int, required=True, help="entropy-label-number")
args = parser.parse_args()
path='../bin/preprocessed_data/cora_entropy_label'+str(args.label)
save_cora(path,args.label)