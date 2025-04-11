import os
import argparse

from optlearn.data import data_utils
from common import *

from multiprocessing import Process

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
        data_utils.build_training_data_for_problem(
            problem_filename.split('.')[0],
            problems_dir,
            training_dir,
            solutions_dir,
            feature_names,
            logger,
        )
    
    # self.data_steps(name)
    # p = Process(target=self.data_steps, args=(name,))
    # p.start()
    # p.join()
