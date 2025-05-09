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
from optlearn.train.model_utils import ModelPersister, ModelWrapper

from optlearn.experiments.train_classifier import setup_training_params

model_fname = sorted(os.listdir(MODELS_PATH))[-1]
print(f'Loading latest model {model_fname}')
wrapper = ModelWrapper()
wrapper.load(os.path.join(MODELS_PATH, model_fname))

THRESHOLD = 0.5
# Eval
for class_name in MATILDA_CLASSES:
    print(f'Evaluating on {class_name}')

    dataLoader = DataLoader({
        class_name: matilda_name_stems_range(63, 190) if class_name in MATILDA_HARD_CLASSES else []
    })
    
    X_test = np.vstack(dataLoader.load_features())
    y_test = np.concatenate(dataLoader.load_labels())

    print('Data shapes:')
    print('X_test:', X_test.shape)
    print('y_test:', y_test.shape)

    y_test_pred = (wrapper.predict_proba_vector(X_test) > THRESHOLD).astype(int)

    print("Results: ")
    metrics = {
        "accuracy": train_utils.accuracy(y_test, y_test_pred),
        "false_negative_rate": train_utils.false_negative_rate(y_test, y_test_pred),
        "pruning_rate": train_utils.pruning_rate(y_test_pred),
    }
    printer = pprint.PrettyPrinter(indent=4)
    printer.pprint(metrics)
