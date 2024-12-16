from optlearn.experiments.train_classifier import train_sparsifier
train_files_parent_path = "C:\\Users\\kisla\\Desktop\\TSPPruning\\tsplib-data"  # The parent directory containing subdirectories for feature files,
                                                  # solution files (labels), and weight files (if sample weights are used).

model_name = "logreg"  # Name of the model to use; must be one of the keys in the `models` dictionary 
                       # (e.g., "logreg", "linear_svc", "svc", "knn", "ridge").

model_param_json_path = "C:\\Users\\kisla\\Desktop\\TSPPruning\\tsplib-data\\model_param.json"  # Path to the JSON file containing hyperparameters for the selected model.
                                                     # If None, the script attempts to use a default file from the `param_jsons` dictionary.

train_param_json_path = "C:\\Users\\kisla\\Desktop\\TSPPruning\\tsplib-data\\train_param.json"  # Path to the JSON file specifying training parameters, such as:
                                                     # - directories for feature files
                                                     # - labels/solutions
                                                     # - weights
                                                     # - train/test/validation split proportions
                                                     # - sampling strategies.

model_save_path = "C:\\Users\\kisla\\Desktop\\TSPPruning\\tsplib-data\\model.pkl"  # Path where the trained model and its metadata will be saved after training.
                                             # This is optional; if not specified, the model won't be saved.

threshold = 0.5  # Threshold for making binary predictions when the model supports probabilities (e.g., Logistic Regression).
                 # Predictions above this threshold are classified as 1; below as 0. Optional.

sample_weights = "C:\\Users\\kisla\\Desktop\\TSPPruning\\tsplib-data\\weights.json"  # Path to the file containing sample weights, which may be used during training
                                                 # to emphasize or de-emphasize certain samples. Optional.
train_sparsifier(
    train_files_parent_path=train_files_parent_path,
    model_name=model_name,
    model_param_json_path=model_param_json_path,
    train_param_json_path=train_param_json_path,
    model_save_path=model_save_path,
    threshold=threshold,
    sample_weights=None,
)