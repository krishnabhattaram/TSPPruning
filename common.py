DATA_DIR = 'tsplib-data' # Relative to this file
# These directories are all relative to DATA_DIR
PROBLEMS_DIR = 'problems' # Input: problems
SOLUTIONS_DIR = 'solutions' # Input: precomputed solutions
TRAINING_DIR = 'training' # Output: features (and maybe labels)

import os
JSONS_PATH = os.path.join(os.path.abspath(''), 'optlearn', 'experiments', 'jsons')
DATA_PATH = os.path.join(os.path.abspath(''), DATA_DIR)
PROBLEMS_PATH = os.path.join(DATA_PATH, PROBLEMS_DIR)
SOLUTIONS_PATH = os.path.join(DATA_PATH, SOLUTIONS_DIR)
TRAINING_PATH = os.path.join(DATA_PATH, TRAINING_DIR)

def build_directories_if_needed():
	print('Building data directories...')
	for path in (PROBLEMS_PATH, SOLUTIONS_PATH, TRAINING_PATH):
		if os.path.exists(path):
			print('Directory already exists:', path)
		else:
			os.mkdir(path)
			print('Created directory:', path)

import json
TRAINING_PARAMS_JSON_PATH = os.path.join(JSONS_PATH, 'training_params.json')
with open(TRAINING_PARAMS_JSON_PATH, "r") as json_file:
	DESIRED_EDGE_FEATURES = json.load(json_file)['feature_dirs']

import shutil
import sys
def clear_directory(path):
	files = os.listdir(path)
	if len(files) == 0:
		return
	if input(f'The output directory {path} is nonempty. Would you like to clear it? (y/n) ').lower() != 'y':
		print('Aborted')
		sys.exit(-1)
	for filename in files:
		file_path = os.path.join(path, filename)
		if os.path.isfile(file_path) or os.path.islink(file_path):
			os.unlink(file_path)
		elif os.path.isdir(file_path):
			shutil.rmtree(file_path)
	print('Cleared directory')
