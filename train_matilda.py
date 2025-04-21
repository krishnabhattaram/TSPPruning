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

from optlearn.data import data_utils
from optlearn.train import train_utils
from optlearn.train import model_utils

from optlearn.experiments.train_classifier import setup_training_params

model = SVC(
    verbose=True,
    class_weight={
        0: 0.01,
        1: 0.99
    },
    kernel='rbf',
    tol=0.001,
)
train_params = setup_training_params(TRAINING_PATH, TRAINING_PARAMS_JSON_PATH)

threshold = 0.5

sample_weights = os.path.join(DATA_PATH, 'weights.json')

model_save_path = os.path.join(
	DATA_PATH,
	'models',
	'model_' + datetime_filename() + '.pkl'
)

train_tuples = data_utils.dataMatcher(
    train_params["feature_dirs"],
    train_params["solution_dir"],
    train_params["weight_dir"],
).build_fname_pairs()

print(train_tuples)

train_loader = data_utils.dataLoader(train_tuples)
# train_loader.train_test_val_split(0.85, 0.10, 0.05)


if "undersampling_strategy" in train_params:
    sampler = RandomUnderSampler(**train_params["undersampling_strategy"])
if "oversampling_strategy" in train_params:
    sampler = RandomOverSampler(**train_params["oversampling_strategy"])
if "oversampling_strategy" in train_params and "undersampling_strategy" in train_params:
    print("Over and undersampling strategies found, defaulting to undersampling!")
    sampler = RandomUnderSampler()
if "oversampling_strategy" not in train_params and "undersampling_strategy" not in train_params:
    print("Neither over nor undersampling strategies found, defaulting to undersampling!")
    sampler = RandomUnderSampler()

function_names = [
    "compute_{}_edges".format(os.path.basename(item))
    for item in train_params["feature_dirs"]
]

X_train, y_train = train_loader.load_training_features(), train_loader.load_training_labels()
X_train, y_train = np.vstack(X_train), np.concatenate(y_train)
# X_train, y_train = sampler.fit_resample(X_train, y_train)

if sample_weights is not None:
    z_train = np.concatenate(train_loader.load_training_weights())
    print(z_train.shape)
    # z_train, y_train = sampler.fit_resample(z_train, y_train)
    model.fit(X_train, y_train, z_train)
else:
    model.fit(X_train, y_train)

wrapper = model_utils.modelWrapper(
    model=model,
    function_names=function_names,
    threshold=threshold
)

printer = pprint.PrettyPrinter(indent=4)

X_test, y_test = train_loader.load_testing_features(), train_loader.load_testing_labels()
X_test, y_test = np.vstack(X_test), np.concatenate(y_test)

if threshold is not None:
    y_test_pred = (wrapper.predict_proba_vector(X_test) > threshold).astype(int)
else:
    y_test_pred = wrapper.predict_vector(X_test)

metrics = {
    "accuracy": train_utils.accuracy(y_test, y_test_pred),
    "false_negative_rate": train_utils.false_negative_rate(y_test, y_test_pred),
    "pruning_rate": train_utils.pruning_rate(y_test_pred),
}

print("Results: ")
printer.pprint(metrics)

if model_save_path is not None:
    persister = model_utils.modelPersister(
        model=model,
        function_names=function_names,
        threshold=threshold
    )
    persister.save(model_save_path)
    print("Model saved at {}".format(model_save_path))

print("Done! :D")
