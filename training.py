# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-23

# Load data for Google_Home dataset for training
import pickle
import time

import numpy as np
from keras.optimizers import Adamax
from keras.utils import np_utils

from utils import load_data_google_home
from Model_def import DFNet


def training_google_home(epoch, batch_size, length, nb_classes):
    description = "Training and evaluating DF model for Google_Home dataset"
    print(description)

    optimizer = Adamax(learning_rate=0.002, beta_1=0.9, beta_2=0.999)
    input_shape = (length, 1)
    verbose = 1

    X_train, y_train, X_test, y_test = load_data_google_home()

    # consider them as float and normalize
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    y_train = y_train.astype('float32')
    y_test = y_test.astype('float32')

    # we need a [Length x 1] x n shape as input to the DFNet (Tensorflow)
    X_train = X_train[:, :, np.newaxis]
    X_test = X_test[:, :, np.newaxis]

    print(X_train.shape[0], 'training samples')
    print(X_test.shape[0], 'validation samples')

    # convert class vectors to binary class matrices
    y_train = np_utils.to_categorical(y_train, nb_classes)
    y_test = np_utils.to_categorical(y_test, nb_classes)

    print("Preparing Data for training")
    # initialize the optimizer and model
    print(time.sleep(2))
    model = DFNet.build(input_shape=input_shape, classes=nb_classes)

    model.compile(loss="categorical_crossentropy", optimizer=optimizer,
                  metrics=["accuracy"])

    print("Model compiled")

    # Start training
    history = model.fit(X_train, y_train,
                        batch_size=batch_size, epochs=epoch, verbose=verbose,
                        validation_data=(X_test, y_test))

    # Save model
    print("Saving Model")
    savedpath = "/home/snape/Documents/comp5703/trained_model/Google_Home"
    model.save(savedpath)
    print("Saving Model Done!", savedpath)


if __name__ == '__main__':
    # epoch, batch_size, length, nb_classes
    training_google_home(20, 64, 600, 11)
