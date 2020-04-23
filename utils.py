# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-23
import os
import pickle

import numpy as np
from sklearn.model_selection import train_test_split


def create_dataset(out_dir):
    data_path = os.path.join(out_dir, "data.pkl")
    data = np.array(pickle.load(data_path))

    labels_path = os.path.join(out_dir, "labels.pkl")
    labels = np.array(pickle.load(labels_path))

    # Randomly shuffle data and labels with corresponding order.
    idx = np.random.permutation(len(data))
    data = np.array()
    X, y = data[idx], labels[idx]

    # Split the dataset into training set and test set in 7:3
    # TODO: add validation dataset

    X_training, X_test, y_training, y_test = train_test_split(X, y, test_size=0.3)

    X_training_outfile = open(os.path.join(out_dir, "X_training.pkl"), 'wb')
    pickle.dump(X_training, X_training_outfile)

    y_training_outfile = open(os.path.join(out_dir, "y_training.pkl"), 'wb')
    pickle.dump(y_training, y_training_outfile)

    X_test_outfile = open(os.path.join(out_dir, "X_test.pkl"), 'wb')
    pickle.dump(X_test, X_test_outfile)

    y_test_outfile = open(os.path.join(out_dir, "y_test.pkl"), 'wb')
    pickle.dump(y_test, y_test_outfile)


if __name__ == '__main__':
    out_dir = "/home/snape/Documents/comp5703/pickle_data/Google_Home/Captures_5m"
    create_dataset(out_dir)