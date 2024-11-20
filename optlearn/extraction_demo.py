import os
from networkx import Graph, draw

DATA_DIR = './tsplib-data'
PROBLEMS_DIR = os.path.join(DATA_DIR, 'problems')
FEATURES_DIR = os.path.join(DATA_DIR, 'npy')
# See the functions dict (line 478) in ./optlearn/optlearn/feature/features.py
# For any feature computation function named compute_fX_edges, you can add fX here
DESIRED_EDGE_FEATURES = ['fa', 'fb', 'fc', 'fd', 'fe', 'ff']
DRAW = False # Display edges with weights and features in build_features

from optlearn.experiments.build_data import build_features
build_features(FEATURES_DIR, PROBLEMS_DIR, DESIRED_EDGE_FEATURES, draw=DRAW)
