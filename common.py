import os
JSONS_PATH = os.path.join(os.path.abspath(''), 'optlearn', 'experiments', 'jsons')
DATA_PATH = os.path.join(os.path.abspath(''), 'data') # ./data
PROBLEMS_PATH = os.path.join(DATA_PATH, 'problems')
GENERATED_PROBLEMS_PATH = os.path.join(PROBLEMS_PATH, 'generated')
SOLUTIONS_PATH = os.path.join(DATA_PATH, 'solutions')
TRAINING_PATH = os.path.join(DATA_PATH, 'training')
MODELS_PATH = os.path.join(DATA_PATH, 'models')

def build_directory(path):
	if os.path.exists(path):
		return
	os.mkdir(path)
	print('Created directory:', path)

def build_level_1_directories():
	for path in (DATA_PATH, PROBLEMS_PATH, SOLUTIONS_PATH, TRAINING_PATH, MODELS_PATH):
		build_directory(path)

# Will exit the program if the directories are nonempty
def build_level_2_directories():
	OUTPUT_PATHS = (SOLUTIONS_PATH, TRAINING_PATH)
	for level_1_dir in OUTPUT_PATHS:
		clear_directory(level_1_dir)
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
