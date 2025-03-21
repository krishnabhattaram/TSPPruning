from common import *
build_level_1_directories()

# Uses fg weights of 1/iteration (1-indexed) instead of iteration/k
USE_PAPER_FG = True

# Builds the ground truth labels directory (tsplib-data/npy/solutions/) along with the features directories
BUILD_LABELS = True

VERBOSE = False

from optlearn.data.data_utils import dataLoader
loader = dataLoader([])

import optlearn.mst.mst_model
optlearn.mst.mst_model.use_paper_fg = USE_PAPER_FG

import numpy as np
np.set_printoptions(linewidth=np.inf)

from optlearn.experiments.build_data import build_features

OUTPUT_PATHS = (SOLUTIONS_PATH, TRAINING_PATH)
for level_1_dir in OUTPUT_PATHS:
	clear_directory(level_1_dir)
for problem_class in os.listdir(PROBLEMS_PATH):
	problems_class_path = os.path.join(PROBLEMS_PATH, problem_class)
	training_class_path = os.path.join(TRAINING_PATH, problem_class)
	solutions_class_path = os.path.join(SOLUTIONS_PATH, problem_class)
	build_directory(training_class_path)
	build_directory(solutions_class_path)
	build_features(
		training_class_path,
		problems_class_path,
		DESIRED_EDGE_FEATURES,
		solution_dir=solutions_class_path,
		verbose=VERBOSE,
		build_labels=BUILD_LABELS
	)
