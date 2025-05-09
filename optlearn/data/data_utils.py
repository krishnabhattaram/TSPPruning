import os
import joblib

import numpy as np
# import networkx as nx

from optlearn import io_utils
from optlearn import graph_utils

from optlearn.feature import features
from optlearn.feature import feature_utils
from optlearn.data import compute_solutions

from sklearn.model_selection import train_test_split

from multiprocessing import Process

from common import *

class DataLoader():
    def __init__(
        self,
        name_stems_per_class: dict[str, list[str]]
    ):
        self.feature_path_tuples = []
        self.label_paths = []
        self.sample_weight_paths = []
        num_total_files = 0
        print('Input files per class:')
        for class_name, name_stems in name_stems_per_class.items():
            class_path = os.path.join(NPY_PATH, class_name)
            num_class_files = 0
            # For empty name_stems lists, default to loading all name stems in the <class>/solutions directory
            if name_stems == []:
                name_stems = sorted([fname[:-4] for fname in os.listdir(os.path.join(class_path, LABEL_DIR))])
            for name_stem in name_stems:
                file_name = name_stem + '.npy'
                self.feature_path_tuples.append(tuple(
                    os.path.join(class_path, feature_dir, file_name)
                    for feature_dir in FEATURE_DIRS
                ))
                self.label_paths.append(os.path.join(class_path, LABEL_DIR, file_name))
                self.sample_weight_paths.append(os.path.join(class_path, WEIGHT_DIR, file_name))
                num_class_files += 1
            print(f'{class_name}: {num_class_files}')
            num_total_files += num_class_files
        print('-')
        print(f'TOTAL: {num_total_files}')

    # def train_test_val_split(self, train=0.7, test=0.15, val=0.15):
    #     """ Generate the train, test and validation sets """

    #     self.train_pairs, self.test_pairs = train_test_split(self.data_pairs, train_size=train)
    #     ratio = test / (test + val)
    #     self.test_pairs, self.val_pairs = train_test_split(self.test_pairs, train_size=ratio)

    def load_features(self, feature_fnames):
        """ Load the features """

        features = [np.load(fname) for fname in feature_fnames]
        return np.stack(features, axis=1)

    def load_labels(self, label_fname):
        """ Load the labels """

        return np.load(label_fname)
    
    def load_weights(self, weight_fname):
        """ Load the weights """

        return np.load(weight_fname)

    def load_pair(self, pair):
        """ Load the feature-label pair """

        features = self.load_features(pair[0])
        labels = self.load_labels(pair[1])
        return features, labels
        
    def load_features(self):
        return [
            np.stack([np.load(feature_path) for feature_path in feature_path_tuple], axis=1)
            for feature_path_tuple in self.feature_path_tuples
        ]

    def load_labels(self):
        return [
            np.load(label_path) for label_path in self.label_paths
        ]
    
    def load_weights(self):
        return [
            np.load(sample_weight_path) for sample_weight_path in self.sample_weight_paths
        ]
