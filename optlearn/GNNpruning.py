import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data, Dataset

DATA_DIR = 'tsp-data'
from optlearn.experiments.build_data import build_features

class TSPDataset(Dataset):
    """Dataset class for TSP instances.
    
    Loads computed features (fa-ff, fi, fj, fg) for each graph.
    Features are computed using build_features() and stored in features_dir.
    """
    def __init__(self, features_dir):
        super().__init__()
        self.features_dir = features_dir
        self.files = os.listdir(features_dir)
        
    def len(self):
        return len(self.files)
        
    def get(self, idx):
        features = torch.load(os.path.join(self.features_dir, self.files[idx]))
        edge_index = features['edge_index']
        edge_attr = features['edge_features']  # [fa-ff, fi, fj, fg]
        y = features['labels']  # 1 for edges in optimal tour, 0 otherwise
        return Data(edge_index=edge_index, edge_attr=edge_attr, y=y)

class TSPPruningGNN(nn.Module):
    """GNN for TSP edge pruning.
    
    Uses two graph convolution layers followed by edge classification MLP.
    Trained with weighted BCE loss to handle class imbalance.
    """
    def __init__(self, num_features=9):  # 9 features: fa-ff, fi, fj, fg
        super().__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.conv2 = GCNConv(64, 32)
        self.edge_classifier = nn.Sequential(
            nn.Linear(32*2, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.softmax()
        )

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        h = self.conv1(x, edge_index)
        h = F.relu(h)
        h = F.dropout(h, p=0.5, training=self.training)
        h = self.conv2(h, edge_index)
        row, col = edge_index
        edge_rep = torch.cat([h[row], h[col]], dim=1)
        scores = self.edge_classifier(edge_rep)
        return scores
    
    def predict(self, graph): 
        PROBLEMS_DIR = os.path.join(DATA_DIR, 'problems')
        FEATURES_DIR = os.path.join(DATA_DIR, 'features')
        DESIRED_EDGE_FEATURES = ['fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fi', 'fj', 'fg']
        features = build_features(FEATURES_DIR, PROBLEMS_DIR, DESIRED_EDGE_FEATURES)

        scores = self.model(features)

        predictions = (scores > self.threshold).float()
        return predictions 

def calculate_num_epochs(train_dataset):
    """Calculate number of epochs based on dataset size."""
    batch_size = 32
    n_iters = 3000
    return int(n_iters // (len(train_dataset) / batch_size))

def train_model(train_graphs, optimal_tours):
    """Train GNN model for TSP edge pruning.
    
    Implements training loop with:
    - Feature computation using fa-ff, fi, fj, fg
    - Binary cross entropy loss with class weights {0.01, 0.99}
    - Edge weight-based sample weights
    - Random undersampling of negative class
    """
    # Setup directories and compute features
    PROBLEMS_DIR = os.path.join(DATA_DIR, 'problems')
    FEATURES_DIR = os.path.join(DATA_DIR, 'features')
    DESIRED_EDGE_FEATURES = ['fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fi', 'fj', 'fg']
    build_features(FEATURES_DIR, PROBLEMS_DIR, DESIRED_EDGE_FEATURES)

    

    
    # Create dataset and model
    dataset = TSPDataset(FEATURES_DIR)
    model = TSPPruningGNN()
    optimizer = torch.optim.Adam(model.parameters())
    criterion = nn.BCELoss(weight=torch.tensor([0.01, 0.99]))
    
    NUM_EPOCHS = calculate_num_epochs(len(dataset))
    
    for epoch in range(NUM_EPOCHS):
        for data in dataset:
            # Get edge weights for sample weighting
            weights = data.edge_attr[:, 0] / data.edge_attr[:, 0].max()
            
            # Forward pass
            scores = model(data)
            loss = criterion(scores, data.y)
            loss = (loss * weights).mean()
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    return model
