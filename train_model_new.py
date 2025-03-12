from common import *
import os
from optlearn.experiments.train_classifier import train_sparsifier
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model_name", nargs="?", default='logreg')
    # Name of the model to use; must be one of the keys in the `models` dictionary 
    # (e.g., "logreg", "linear_svc", "svc", "knn", "ridge").
    parser.add_argument("-p", "--model_param_json_path", nargs="?", default=None)
    # Path to the JSON file containing hyperparameters for the selected model.
    # If None, the script attempts to use a default file from the `param_jsons` dictionary.
    parser.add_argument("-t", "--train_param_json_path", nargs="?", default=TRAINING_PARAMS_JSON_PATH)
    # Path to the JSON file specifying training parameters, such as:
    # - directories for feature files
    # - labels/solutions
    # - weights
    # - train/test/validation split proportions
    # - sampling strategies.
    parser.add_argument("-f", "--train_files_parent_path", nargs="?", default=TRAINING_PATH)

    parser.add_argument("-s", "--model_save_path", nargs="?", default=os.path.join(DATA_PATH, 'model.pkl'))
    # Path where the trained model and its metadata will be saved after training.
    # This is optional; if not specified, the model won't be saved.
    parser.add_argument("-y", "--threshold", nargs="?", default=0.5)
    # Threshold for making binary predictions when the model supports probabilities (e.g., Logistic Regression).
    # Predictions above this threshold are classified as 1; below as 0. Optional.
    parser.add_argument("-w", "--sample_weights", nargs="?", default=os.path.join(DATA_PATH, 'weights.json'))
    # Path to the file containing sample weights, which may be used during training
    # to emphasize or de-emphasize certain samples. Optional.
    
    train_sparsifier(**vars(parser.parse_args()))
