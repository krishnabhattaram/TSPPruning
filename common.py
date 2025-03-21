import os
import logging

JSONS_PATH = os.path.join(os.path.abspath(''), 'optlearn', 'experiments', 'jsons')
DATA_PATH = os.path.join(os.path.abspath(''), 'data') # ./data
PROBLEMS_PATH = os.path.join(DATA_PATH, 'problems')
GENERATED_PROBLEMS_PATH = os.path.join(PROBLEMS_PATH, 'generated')
SOLUTIONS_PATH = os.path.join(DATA_PATH, 'solutions')
TRAINING_PATH = os.path.join(DATA_PATH, 'training')
MODELS_PATH = os.path.join(DATA_PATH, 'models')
LOGS_PATH = os.path.join(DATA_PATH, 'logs')

import shutil
import sys
def clear_directories(paths):
    paths_to_clear = [path for path in paths if len(os.listdir(path)) > 0]
    if len(paths_to_clear) == 0:
        return
    
    if input('\n'.join([
        'These output directories are nonempty and need to be cleared:',
        *paths_to_clear,
        'Proceed? (y/n) '
    ])).lower() != 'y':
        print('Aborted')
        sys.exit(-1)
    for path in paths_to_clear:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print(f'Cleared directory {path}')

def build_directory(path):
    if os.path.exists(path):
        return
    os.mkdir(path)
    print('Created directory:', path)

def build_level_1_directories():
    for path in (DATA_PATH, PROBLEMS_PATH, SOLUTIONS_PATH, TRAINING_PATH, MODELS_PATH, LOGS_PATH):
        build_directory(path)

# Will exit the program if the directories are nonempty
def build_level_2_directories():
    OUTPUT_PATHS = (SOLUTIONS_PATH, TRAINING_PATH)
    clear_directories(OUTPUT_PATHS)
    for level_1_dir in OUTPUT_PATHS:
        for problem_class in os.listdir(PROBLEMS_PATH):
            build_directory(os.path.join(level_1_dir, problem_class))

def build_generated_problems_directory():
    build_level_1_directories()
    build_directory(GENERATED_PROBLEMS_PATH)

import json
TRAINING_PARAMS_JSON_PATH = os.path.join(JSONS_PATH, 'training_params.json')
with open(TRAINING_PARAMS_JSON_PATH, "r") as json_file:
    DESIRED_EDGE_FEATURES = json.load(json_file)['feature_dirs']

from datetime import datetime
def datetime_filename():
    return datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

def log_datetime(file, txt):
    file.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S | ') + txt + '\n')

# Adapted from https://stackoverflow.com/a/28330410
def setup_custom_logger(log_path, name):
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler = logging.FileHandler(log_path, mode='w')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logging.getLogger(name)
