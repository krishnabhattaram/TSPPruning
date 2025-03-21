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

clear_directories([SOLUTIONS_PATH, TRAINING_PATH])

log_path = os.path.join(LOGS_PATH, datetime_filename() + '.txt')
with open(log_path, 'w') as f:
	logger = setup_custom_logger(log_path, 'logger')
	logger.info('Started training data computation')
	problem_classes = os.listdir(PROBLEMS_PATH)
	for i, problem_class in enumerate(problem_classes):
		logger.info(f'({i + 1}/{len(problem_classes)}) Starting problem class {problem_class}')
		problems_class_path = os.path.join(PROBLEMS_PATH, problem_class)
		training_class_path = os.path.join(TRAINING_PATH, problem_class)
		solutions_class_path = os.path.join(SOLUTIONS_PATH, problem_class)
		build_directory(training_class_path)
		build_directory(solutions_class_path)
		build_features(
			training_class_path,
			problems_class_path,
			DESIRED_EDGE_FEATURES,
			logger,
			solution_dir=solutions_class_path,
			verbose=VERBOSE,
			build_labels=BUILD_LABELS
		)
	logger.info('Done')
