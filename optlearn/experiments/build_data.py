import os

import numpy as np

from optlearn import io_utils
from optlearn import graph_utils

from optlearn.feature import features
from optlearn.feature import feature_utils
from optlearn.data import compute_solutions

from sklearn.model_selection import train_test_split

from multiprocessing import Process
from common import *



def build_training_data_for_class(
    problems_dir,
    training_dir,
    solutions_dir,
    feature_names,
    logger,
):
    """ 
    Given a directory to write numpy files to and a directory from which to pick up
    problem instances, build the specified features and write them into separate npy
    files for feature for eahc problem instance.
    """

    # Build feature/solution dirs
    for feature_name in feature_names:
        build_directory(os.path.join(training_dir, feature_name))
    build_directory(os.path.join(training_dir, 'solutions'))

    # Process individual problems
    problem_filenames = sorted(os.listdir(problems_dir))
    for i, problem_filename in enumerate(problem_filenames):
        logger.info(f'\t({i + 1}/{len(problem_filenames)}) Starting {problem_filename}')
        data_utils.build_training_data_for_problem_wrapper(
            problem_filename.split('.')[0],
            problems_dir,
            training_dir,
            solutions_dir,
            feature_names,
            logger,
        )
