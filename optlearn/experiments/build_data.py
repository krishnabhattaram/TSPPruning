import os
import argparse

from optlearn.data import data_utils


def build_features(
    numpy_dir,
    problem_dir,
    features,
    override=False,
    solution_dir=None,
    verbose=True,
    build_labels=True
):
    """ 
    Given a directory to write numpy files to and a directory from which to pick up
    problem instances, build the specified features and write them into separate npy
    files for feature for eahc problem instance.
    """

    problems, solutions = [], []
    solution_files = set(os.listdir(solution_dir) if solution_dir else [])
    for problem_file in os.listdir(problem_dir):
        problems.append(os.path.join(problem_dir, problem_file))
        expected_solution_file = problem_file.replace('.tsp', '.opt.tour')
        if expected_solution_file in solution_files:
            solutions.append(os.path.join(solution_dir, expected_solution_file))
        else:
            solutions.append(None)
        
    file_pairs = list(zip(problems, solutions))

    features = ["compute_{}_edges".format(item) for item in features]


    builder = data_utils.createTrainingFeatures(
        numpy_dir,
        features,
        file_pairs,
        override=override,
        verbose=verbose,
        build_labels=build_labels
    )
    builder.data_create()

    print("Done! :D")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--numpy_dir", nargs="?", required=True)
    parser.add_argument("-p", "--problem_dir", nargs="?", required=True)
    parser.add_argument("-f", "--features", nargs="+", required=True)
    
    build_features(**vars(parser.parse_args()))
