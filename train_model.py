from common import *
import os
from optlearn.experiments.train_classifier import train_sparsifier

train_files_parent_path = TRAINING_PATH

model_name = 'logreg'
# Name of the model to use; must be one of the keys in the `models` dictionary 
# (e.g., "logreg", "linear_svc", "svc", "knn", "ridge").

MODEL_PARAM_JSON_PATH = None
# Path to the JSON file containing hyperparameters for the selected model.
# If None, the script attempts to use a default file from the `param_jsons` dictionary.

train_param_json_path = TRAINING_PARAMS_JSON_PATH
# Path to the JSON file specifying training parameters, such as:
# - directories for feature files
# - labels/solutions
# - weights
# - train/test/validation split proportions
# - sampling strategies.

model_save_path = os.path.join(DATA_PATH, 'model.pkl')
# Path where the trained model and its metadata will be saved after training.
# This is optional; if not specified, the model won't be saved.

threshold = 0.5
# Threshold for making binary predictions when the model supports probabilities (e.g., Logistic Regression).
# Predictions above this threshold are classified as 1; below as 0. Optional.

sample_weights = os.path.join(DATA_PATH, 'weights.json')
# Path to the file containing sample weights, which may be used during training
# to emphasize or de-emphasize certain samples. Optional.

train_sparsifier(
    train_files_parent_path=train_files_parent_path,
    model_name=model_name,
    model_param_json_path=MODEL_PARAM_JSON_PATH,
    train_param_json_path=train_param_json_path,
    model_save_path=model_save_path,
    threshold=threshold,
    sample_weights=None,
)
