# Author: Sally Kang <snapekang@gmail.com>
# Created: 20-4-23

import time

import numpy as np
from keras.optimizers import Adamax
from keras.optimizers import Adam
from keras.optimizers import SGD

from keras.utils import np_utils

from utils import load_data
from Model_def import DFNet
from sklearn import preprocessing
import os
import matplotlib.pyplot as plt


def training(dataset_dir, save_path, lr, epoch, batch_size, input_length, nb_classes):
    dataset_type = os.path.basename(os.path.dirname(dataset_dir)) + "_" + os.path.basename(dataset_dir)
    description = "Training and evaluating DF model for "
    print(description + dataset_type)

    optimizer = Adamax(learning_rate=lr, beta_1=0.9, beta_2=0.999)
    # optimizer = SGD(learning_rate=lr)
    input_shape = (input_length, 1)
    verbose = 1

    X_train, y_train, X_val, y_val, X_test, y_test = load_data(dataset_dir)

    # consider them as float and normalize
    X_train = X_train.astype('float32')
    X_val = X_val.astype('float32')
    X_test = X_test.astype('float32')
    y_train = y_tr6ain.astype('float32')
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
    fig_title = "DF Model with " + "lr=" + str(lr) + " batch_size=" + str(batch_size)

    fig, ax1 = plt.subplots()
    fig.suptitle(fig_title, y=1.05)
    ax1.set_xlabel('epoch')
    ax1.set_ylabel('accuracy')
    l1, = ax1.plot(history.history['accuracy'], color='r', marker=".")
    l2, = ax1.plot(history.history['val_accuracy'], color='b', marker="v")
    ax2 = ax1.twinx()
    ax2.set_ylabel('loss')
    l3, = ax2.plot(history.history['loss'], color='g', marker="*")
    l4, = ax2.plot(history.history['val_loss'], color='y', marker="X")
    plt.legend([l1, l2, l3, l4], ['DF Training Accuracy', 'DF Testing Accuracy', 'DF Training Loss', 'DF Testing Loss'],
               loc='center right')

    fig.tight_layout()
    # plt.savefig(fig_title + '.png')
    plt.show()


if __name__ == '__main__':
    # Training Google_Home dataset
    dataset_dir = "/home/snape/Documents/comp5703/pickle_data/Amazon_Echo/April18"
    save_path = "/home/snape/Documents/comp5703/trained_models"
    lr = 0.0001
    epoch = 50
    batch_size = 32
    input_length = 300
    nb_classes = 10
    # lr_range = [0.0001, 0.001, 0.002, 0.01, 0.02]
    # batch_size_range = [64, 128, 256]
    # for lr in lr_range:
    training(dataset_dir, save_path, lr, epoch, batch_size, input_length, nb_classes)
