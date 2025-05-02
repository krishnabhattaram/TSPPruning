from common import *
build_level_1_directories()

# Uses fg weights of 1/iteration (1-indexed) instead of iteration/k
USE_PAPER_FG = True

from optlearn.data.data_utils import DataLoader
loader = DataLoader([])

import optlearn.mst.mst_model
optlearn.mst.mst_model.use_paper_fg = USE_PAPER_FG

import numpy as np
np.set_printoptions(linewidth=np.inf)

from optlearn import io_utils
from optlearn import graph_utils

from optlearn.feature import features
from optlearn.data import compute_solutions

from multiprocessing import Process

def build_training_data_for_problem(
    namestem,
    problems_dir,
    training_dir,
    solutions_dir,
    feature_names,
    logger,
):
    logging.getLogger().setLevel(logging.INFO)

    problem_path = os.path.join(problems_dir, namestem + '.tsp')

    object = io_utils.optObject()
    object.read_problem_from_file(problem_path)
    graph = object.get_graph()

    # Features
    for feature_name in feature_names:
        feature_path = os.path.join(training_dir, feature_name, namestem + '.npy')
        if os.path.exists(feature_path):
            logger.info(f'\t\t Feature {feature_name}: skipping')
        else:
            logger.info(f'\t\t Feature {feature_name}: computing')
            data = features.functions[f'compute_{feature_name}_edges'](graph)
            np.save(feature_path, data)
    
    # Solution (npy)
    solution_path = os.path.join(solutions_dir, namestem + '.opt.tour')
    labels_path = os.path.join(training_dir, 'solutions', namestem + '.npy')
    if os.path.exists(labels_path):
        logger.info(f'\t\t Solution: skipping')
    else:
        logger.info(f'\t\t Solution: computing')
        if os.path.exists(solution_path):
            tour = object.read_solution_from_file(solution_path)
            edges = graph_utils.get_tour_edges(tour)
            min_vertex = np.min(graph.nodes)
            order = len(graph.nodes)
            indices = [
                graph_utils.compute_vector_index_symmetric(edge, order, min_vertex)
                for edge in edges
            ]
            data = np.zeros(len(graph.edges))
            data[indices] = 1
        else:
            data = compute_solutions.get_all_optimal_tsp_solutions(graph)
        np.save(labels_path, data)
    
    # Sample weights
    sample_weights_path = os.path.join(training_dir, 'sample_weights', namestem + '.npy')
    if os.path.exists(sample_weights_path):
        logger.info(f'\t\t Sample weights: skipping')
    else:
        logger.info(f'\t\t Sample weights: computing')
        weights = np.array(graph_utils.get_weights(graph))
        global_max = weights.max()
        np.save(sample_weights_path, weights / global_max)

if __name__ == '__main__':
    ask_to_clear_directories([SOLUTIONS_PATH, NPY_PATH])
    log_path = os.path.join(LOGS_PATH, datetime_filename() + '.txt')
    logger = setup_custom_logger(log_path, 'logger')
    logger.info('Started npy data computation')
    problem_classes = os.listdir(PROBLEMS_PATH)
    for i, problem_class in enumerate(problem_classes):
        logger.info(f'({i + 1}/{len(problem_classes)}) Starting problem class {problem_class}')
        problems_class_path = os.path.join(PROBLEMS_PATH, problem_class)
        training_class_path = os.path.join(NPY_PATH, problem_class)
        solutions_class_path = os.path.join(SOLUTIONS_PATH, problem_class)
        build_directory(training_class_path)
        build_directory(solutions_class_path)
        
        # Build feature/solution dirs
        for feature_name in FEATURE_DIRS:
            build_directory(os.path.join(training_class_path, feature_name))
        build_directory(os.path.join(training_class_path, 'solutions'))
        build_directory(os.path.join(training_class_path, 'sample_weights'))

        # Process individual problems
        problem_filenames = sorted(os.listdir(problems_class_path))
        for i, problem_filename in enumerate(problem_filenames):
            logger.info(f'\t({i + 1}/{len(problem_filenames)}) Starting {problem_filename}')
            p = Process(
                target=build_training_data_for_problem,
                args=(
                    problem_filename.split('.')[0],
                    problems_class_path,
                    training_class_path,
                    solutions_class_path,
                    FEATURE_DIRS,
                    logger,
                )
            )
            p.start()
            p.join()
    logger.info('Done')
