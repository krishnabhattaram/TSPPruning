import torch
import networkx as nx
import numpy as np
from torch_geometric.data import Data
from optlearn.experiments.build_data import build_features
from GNNpruning import * 

def load_tsp_instance(filename):
    """Load TSP instance from file"""
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    # Parse dimension
    dim = int([l for l in lines if 'DIMENSION' in l][0].split(':')[1])
    
    # Parse matrix
    matrix_start = lines.index('EDGE_WEIGHT_SECTION\n') + 1
    matrix = []
    for i in range(dim):
        row = list(map(int, lines[matrix_start + i].strip().split()))
        matrix.append(row)
    
    # Create graph
    G = nx.Graph()
    for i in range(dim):
        for j in range(i+1, dim):
            G.add_edge(i, j, weight=matrix[i][j])
            
    return G

# Load instance
G = load_tsp_instance('small_tsp_instance.tsp')

# Create data object for GNN
DESIRED_EDGE_FEATURES = ['fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fi', 'fj', 'fg']
features = build_features(G, DESIRED_EDGE_FEATURES)
edge_index = torch.tensor(list(G.edges()), dtype=torch.long).t()
data = Data(x=torch.tensor(features, dtype=torch.float), 
           edge_index=edge_index)

# Pass to model
model = TSPPruningGNN()
predictions = model(data)