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

def problem_pairs_from_fnames(problem_fnames, solution_fnames=None):
    """ Build the problem solution pairs for computing features """

    solution_fnames = solution_fnames or [None, ] * len(problem_fnames)
    
    return {problem_fname: solution_fname for
            (problem_fname, solution_fname) in zip(problem_fnames, solution_fnames)}

def get_pair_name(pair):
    """ Assign a name to a problem-solution pair """

    return os.path.basename(pair[0])

class dataMatcher():

    def __init__(self, feature_dirs, solution_dir, weight_dir, name_stems: dict[str, list[str]]=None):
        self.feature_dirs = feature_dirs
        self.solution_dir = solution_dir
        self.weight_dir = weight_dir

        self.name_stems = name_stems
        # TODO add automatic name stems per class
        # if specific_name_stems is None:
        #     some_fnames = self._get_fnames(self.feature_dirs[0])
        #     self.name_stems = self._get_file_stems(some_fnames)

    def _get_file_stems(self, fnames):
        """ Get the name stem of files """

        return [os.path.basename(fname).split('.')[0] for fname in fnames]

    def _get_fnames(self, directory):
        """ Get the absolute paths for the fnames in the given directory """

        fnames = os.listdir(directory)
        return [os.path.join(directory, fname) for fname in fnames]
            
    def _build_fnames_directory(self, directory):
        """ Build the fnames for a given directory """ 

        return [
            os.path.join(directory, stem + '.npy')
            for stem in self.name_stems
        ]

    def build_fname_pairs(self):
        """ Build the pairs of feature fnames and solution fname """

        feature_fname_tuples = [
            self._build_fnames_directory(directory) for directory in self.feature_dirs
        ]
        feature_fname_tuples = list(zip(*feature_fname_tuples))
        solution_fnames = self._build_fnames_directory(self.solution_dir)
        return list(zip(feature_fname_tuples, solution_fnames))

    def build_fname_triples(self):
        
        feature_fname_tuples = [
            self._build_fnames_directory(directory) for directory in self.feature_dirs
        ]
        feature_fname_tuples = list(zip(*feature_fname_tuples))
        solution_fnames = self._build_fnames_directory(self.solution_dir)
        sample_weight_fnames = self._build_fnames_directory(self.weight_dir)
        return list(zip(feature_fname_tuples, solution_fnames, sample_weight_fnames))

    def build_fname_sets(self):
        """ Build the separate lists of feature fnames and solution fnames """

        feature_fname_tuples = [
            self._build_fnames_directory(directory) for directory in self.feature_dirs
        ]
        solution_fnames = self._build_fnames_directory(self.solution_dir)
        return feature_fname_tuples, solution_fnames
    
class DataLoader():
    def __init__(
        self,
        name_stems_per_class: dict[str, list[str]]
    ):
        # TODO add automatic name stems per class?
        # if specific_name_stems is None:
        #     some_fnames = self._get_fnames(self.feature_dirs[0])
        #     self.name_stems = self._get_file_stems(some_fnames)

        self.feature_path_tuples = []
        self.solution_paths = []
        self.sample_weight_paths = []
        for class_name, name_stems in name_stems_per_class.items():
            class_path = os.path.join(NPY_PATH, class_name)
            for name_stem in name_stems:
                file_name = name_stem + '.npy'
                self.feature_path_tuples.append(tuple(
                    os.path.join(class_path, feature_dir, file_name)
                    for feature_dir in FEATURE_DIRS
                ))
                self.solution_paths.append(os.path.join(class_path, SOLUTION_DIR, file_name))
                self.sample_weight_paths.append(os.path.join(class_path, WEIGHT_DIR, file_name))

    def train_test_val_split(self, train=0.7, test=0.15, val=0.15):
        """ Generate the train, test and validation sets """

        self.train_pairs, self.test_pairs = train_test_split(self.data_pairs, train_size=train)
        ratio = test / (test + val)
        self.test_pairs, self.val_pairs = train_test_split(self.test_pairs, train_size=ratio)

    # def train_test_split_matilda(self):
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
        
    def load_training_features(self):
        """ Load the training pairs """

        return [
            self.load_features(pair[0]) for pair in self.train_pairs
        ]

    def load_training_labels(self):
        """ Load the training labels """

        return [
            self.load_labels(pair[1]) for pair in self.train_pairs
        ]

    def load_testing_features(self):
        """ Load the testing pairs """

        return [
            self.load_features(pair[0]) for pair in self.test_pairs
        ]

    def load_testing_labels(self):
        """ Load the testing labels """

        return [
            self.load_labels(pair[1]) for pair in self.test_pairs
        ]

    def load_validation_features(self):
        """ Load the validation pairs """

        return [
            self.load_features(pair[0]) for pair in self.val_pairs
        ]

    def load_validation_labels(self):
        """ Load the validation labels """

        return [
            self.load_labels(pair[1]) for pair in self.val_pairs
        ]

    def load_training_weights(self):
        return [
            self.load_training_weights(pair[0]) for pair in self.train_pairs
        ]
