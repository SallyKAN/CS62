# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-23

import time

import numpy as np
from keras.optimizers import Adamax
from keras.utils import np_utils

from utils import load_data
from Model_def import DFNet
from sklearn import preprocessing
import os
import matplotlib.pyplot as plt

def training(dataset_dir, save_path, epoch, batch_size, length, nb_classes):
    dataset_type = os.path.basename(os.path.dirname(dataset_dir)) + "_" + os.path.basename(dataset_dir)
    description = "Training and evaluating DF model for "
    print(description + dataset_type)

    optimizer = Adamax(learning_rate=0.0001, beta_1=0.9, beta_2=0.999)
    input_shape = (length, 1)
    verbose = 1

    X_train, y_train, X_val, y_val, X_test, y_test = load_data(dataset_dir)

    # consider them as float and normalize
    X_train = X_train.astype('float32')
    X_val = X_val.astype('float32')
    X_test = X_test.astype('float32')
    y_train = y_train.astype('float32')
    y_val = y_val.astype('float32')
    y_test = y_test.astype('float32')

    X_train = preprocessing.normalize(X_train)
    X_val = preprocessing.normalize(X_val)
    X_test = preprocessing.normalize(X_test)

    # we need a [Length x 1] x n shape as input to the DFNet (Tensorflow)
    X_train = X_train[:, :, np.newaxis]
    X_val = X_val[:, :, np.newaxis]
    X_test = X_test[:, :, np.newaxis]

    print(X_train.shape[0], 'training samples')
    print(X_val.shape[0], 'validation samples')
    print(X_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = np_utils.to_categorical(y_train, nb_classes)
    y_val = np_utils.to_categorical(y_val, nb_classes)
    y_test = np_utils.to_categorical(y_test, nb_classes)

    print("Preparing Data for training")
    # initialize the optimizer and model
    print(time.sleep(2))
    # Building and training model
    print("Building and training DF model")
    model = DFNet.build(input_shape=input_shape, classes=nb_classes)

    model.compile(loss="categorical_crossentropy", optimizer=optimizer,
                  metrics=["accuracy"])

    print("Model compiled")

    # Start training
    history = model.fit(X_train, y_train,
                        batch_size=batch_size, epochs=epoch, verbose=verbose,
                        validation_data=(X_val, y_val))

    # Save model
    print("Saving Model")
    savedpath = save_path + "/%s.h5" % str(dataset_type)
    model.save(savedpath)
    print("Saving Model Done!", savedpath)

    score_test = model.evaluate(X_test, y_test, verbose=verbose)
    print("Testing accuracy:", score_test[1])

    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


if __name__ == '__main__':
    # Training Google_Home dataset
    dataset_dir = "/home/snape/Documents/comp5703/pickle_data/Google_Home/Captures_5m"
    save_path = "/home/snape/Documents/comp5703/trained_models"
    training(dataset_dir, save_path, 40, 64, 600, 10)
