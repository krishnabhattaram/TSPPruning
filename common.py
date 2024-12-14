DATA_DIR = 'tsplib-data' # Relative to this file
# These directories are all relative to DATA_DIR
PROBLEMS_DIR = 'problems' # Input: problems
SOLUTIONS_DIR = 'solutions' # Input: precomputed solutions
NP_DIR = 'npy' # Output: features (and maybe labels)

import os
DATA_PATH = os.path.join(os.path.abspath(''), DATA_DIR)
PROBLEMS_PATH = os.path.join(DATA_PATH, PROBLEMS_DIR)
SOLUTIONS_PATH = os.path.join(DATA_PATH, SOLUTIONS_DIR)
NP_PATH = os.path.join(DATA_PATH, NP_DIR)

DESIRED_EDGE_FEATURES = ['fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fg', 'fi', 'fj']

import shutil
def clear_directory(path):
	if input(f'Clear directory {path}? (y/n) ').lower() != 'y':
		return
	for filename in os.listdir(path):
		file_path = os.path.join(path, filename)
		if os.path.isfile(file_path) or os.path.islink(file_path):
			os.unlink(file_path)
		elif os.path.isdir(file_path):
			shutil.rmtree(file_path)
	print('Cleared')
