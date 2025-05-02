import os
import json
import pprint
import pathlib
import argparse

from common import *

import numpy as np

from sklearn.svm import SVC, LinearSVC
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler

from optlearn.data.data_utils import DataLoader
from optlearn.train import train_utils
from optlearn.train import model_utils

from optlearn.experiments.train_classifier import setup_training_params

# TODO: Add l1 regularization?
# only if this accuracy isn't high enough
model = SVC(
    verbose=True,
    class_weight={
        0: 0.01,
        1: 0.99
    },
    kernel='rbf',
    tol=0.001,
)
threshold = 0.5
model_save_path = os.path.join(MODELS_PATH, f'model_{datetime_filename()}.pkl')

dataLoader = DataLoader(
	{class_name: matilda_name_stems_range(1, 64) for class_name in MATILDA_HARD_CLASSES}
)

print(dataLoader.feature_path_tuples)
print(dataLoader.solution_paths)
print(dataLoader.sample_weight_paths)

# train_loader = data_utils.dataLoader(train_tuples)
# # train_loader.train_test_val_split(0.85, 0.10, 0.05)

# sampler = RandomUnderSampler()

# function_names = [f'compute_{feature}_edges' for feature in FEATURE_DIRS]
# # Training
# X_train = np.vstack(dataLoader.load_training_features())
# y_train = np.concatenate(dataLoader.load_training_labels())
# X_train, y_train = sampler.fit_resample(X_train, y_train)
# sample_weights = np.concatenate(dataLoader.load_training_weights())
# sample_weights, y_train = sampler.fit_resample(sample_weights, y_train)

# model.fit(X_train, y_train, sample_weights)

# persister = model_utils.modelPersister(
#     model=model,
#     function_names=function_names,
#     threshold=threshold
# )
# persister.save(model_save_path)
# print(f"Model saved at {model_save_path}")
