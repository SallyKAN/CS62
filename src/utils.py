# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-23
import os
import pickle

import numpy as np
from sklearn.model_selection import train_test_split


def create_dataset(out_dir):
    # Load training data
    data_path = os.path.join(out_dir, "data.pkl")
    with open(data_path, 'rb') as handle:
        data = np.array(pickle.load(handle))

    labels_path = os.path.join(out_dir, "labels.pkl")
    with open(labels_path, 'rb') as handle:
        labels = np.array(pickle.load(handle))

    # Randomly shuffle data and labels with corresponding order.
    idx = np.random.permutation(len(data))
    X, y = data[idx], labels[idx]

    # Split the dataset into train set, test set, and validation set in 6:2:2
    X_training, X_test, y_training, y_test = train_test_split(X, y, test_size=0.2)
    X_training, X_val, y_training, y_val = train_test_split(X_training, y_training, test_size=0.25)  # 0.25 x 0.8 = 0.2

    X_training_outfile = open(os.path.join(out_dir, "X_training.pkl"), 'wb')
    pickle.dump(X_training, X_training_outfile)

    y_training_outfile = open(os.path.join(out_dir, "y_training.pkl"), 'wb')
    pickle.dump(y_training, y_training_outfile)

    X_test_outfile = open(os.path.join(out_dir, "X_test.pkl"), 'wb')
    pickle.dump(X_test, X_test_outfile)

    y_test_outfile = open(os.path.join(out_dir, "y_test.pkl"), 'wb')
    pickle.dump(y_test, y_test_outfile)

    X_val_outfile = open(os.path.join(out_dir, "X_val.pkl"), 'wb')
    pickle.dump(X_val, X_val_outfile)

    y_val_outfile = open(os.path.join(out_dir, "y_val.pkl"), 'wb')
    pickle.dump(y_val, y_val_outfile)


def load_data(dataset_dir):
    print("Loading dataset from " + dataset_dir)
    # dataset_dir = '/home/snape/Documents/comp5703/pickle_data/Google_Home/Captures_5m/'

    # Load training data
    with open(os.path.join(dataset_dir, 'X_training.pkl'), 'rb') as handle:
        X_train = np.array(pickle.load(handle))
    with open(os.path.join(dataset_dir, 'y_training.pkl'), 'rb') as handle:
        y_train = np.array(pickle.load(handle))

    # Load testing data
    with open(os.path.join(dataset_dir, 'X_test.pkl'), 'rb') as handle:
        X_test = np.array(pickle.load(handle))
    with open(os.path.join(dataset_dir, 'y_test.pkl'), 'rb') as handle:
        y_test = np.array(pickle.load(handle))

    # Load validation data
    with open(os.path.join(dataset_dir, 'X_val.pkl'), 'rb') as handle:
        X_val = np.array(pickle.load(handle))
    with open(os.path.join(dataset_dir, 'y_val.pkl'), 'rb') as handle:
        y_val = np.array(pickle.load(handle))

    print("data dimensions:")
    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)

    print("X: Validation data's shape : ", X_val.shape)
    print("y: Validation data's shape : ", y_val.shape)

    print("X: Testing data's shape : ", X_test.shape)
    print("y: Testing data's shape : ", y_test.shape)

    return X_train, y_train, X_val, y_val, X_test, y_test


if __name__ == '__main__':
    # aamazon5_data_dir = "/home/snape/Documents/comp5703/pickle_data/Amazon_Echo/Captures_5m"
    # create_dataset(aamazon5_data_dir)
    #
    # amazon10_data_dir = "/home/snape/Documents/comp5703/pickle_data/Amazon_Echo/Captures_10m"
    # create_dataset(amazon10_data_dir)
    #
    google_out_dir = "/home/snape/Documents/comp5703/pickle_data/Google_Home/May22"
    # create_dataset(google_out_dir)
    # amazon_out_dir = "/home/snape/Documents/comp5703/pickle_data/Amazon_Echo/April18"
    create_dataset(google_out_dir)
