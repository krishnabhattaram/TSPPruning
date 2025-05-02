import os
import logging

# Within each /data/npy/{class}/ directory
FEATURE_DIRS = ["fa", "fb", "fc", "fd", "fe", "ff", "fg", "fi", "fj"]
LABEL_DIR = 'solutions'
WEIGHT_DIR = 'sample_weights'

DATA_PATH = os.path.join(os.path.abspath(''), 'data') # ./data
PROBLEMS_PATH = os.path.join(DATA_PATH, 'problems')
GENERATED_PROBLEMS_PATH = os.path.join(PROBLEMS_PATH, 'generated')
SOLUTIONS_PATH = os.path.join(DATA_PATH, 'solutions')
NPY_PATH = os.path.join(DATA_PATH, 'npy')
MODELS_PATH = os.path.join(DATA_PATH, 'models')
LOGS_PATH = os.path.join(DATA_PATH, 'logs')

MATILDA_HARD_CLASSES = ['CLKhard', 'LKCChard']
MATILDA_NON_HARD_CLASSES = ['CLKeasy', 'easyCLK-hardLKCC', 'hardCLK-easyLKCC', 'LKCCeasy', 'random']
MATILDA_CLASSES = MATILDA_HARD_CLASSES + MATILDA_NON_HARD_CLASSES
def matilda_name_stems_range(start, stop):
    return [f'{i:03}' for i in range(start, stop)]

import shutil
import sys
def ask_to_clear_directories(paths):
    paths_to_clear = [path for path in paths if len(os.listdir(path)) > 0]
    if len(paths_to_clear) == 0:
        return
    
    if input('\n'.join([
        "These output directories are nonempty. Would you like to clear them? If you don't clear them, existing output files will NOT be recomputed.",
        *paths_to_clear,
        '(y/n) '
    ])).lower() != 'y':
        return
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
    for path in (DATA_PATH, PROBLEMS_PATH, SOLUTIONS_PATH, NPY_PATH, MODELS_PATH, LOGS_PATH):
        build_directory(path)

# Will exit the program if the directories are nonempty
def build_level_2_directories():
    OUTPUT_PATHS = (SOLUTIONS_PATH, NPY_PATH)
    ask_to_clear_directories(OUTPUT_PATHS)
    for level_1_dir in OUTPUT_PATHS:
        for problem_class in os.listdir(PROBLEMS_PATH):
            build_directory(os.path.join(level_1_dir, problem_class))

def build_generated_problems_directory():
    build_level_1_directories()
    build_directory(GENERATED_PROBLEMS_PATH)

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
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logging.getLogger(name)
