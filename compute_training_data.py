from common import *
build_directories_if_needed()

clear_directory(TRAINING_PATH)
clear_directory(SOLUTIONS_PATH)

# Uses fg weights of 1/iteration (1-indexed) instead of iteration/k
USE_PAPER_FG = True

# Builds the ground truth labels directory (tsplib-data/npy/solutions/) along with the features directories
BUILD_LABELS = True

VERBOSE = False

from optlearn.data.data_utils import dataLoader
loader = dataLoader([])

import optlearn.mst.mst_model
optlearn.mst.mst_model.use_paper_fg = USE_PAPER_FG

import optlearn.data.data_utils
optlearn.data.data_utils.build_labels = BUILD_LABELS

import numpy as np
np.set_printoptions(linewidth=np.inf)

from optlearn.experiments.build_data import build_features
build_features(
	TRAINING_PATH,
	PROBLEMS_PATH,
	DESIRED_EDGE_FEATURES,
	solution_dir=SOLUTIONS_PATH,
	verbose=VERBOSE
)
