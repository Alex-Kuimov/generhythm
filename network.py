import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.callbacks import ModelCheckpoint

import tensorflow as tf
from tensorflow.keras import layers


def create_network(input_dim, num_features):
    model = tf.keras.Sequential()
    model.add(layers.LSTM(128, input_shape=(None, input_dim)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(num_features, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def train(model, input_data, output_data, epochs=20, batch_size=64, name='data'):
    model.fit(input_data, output_data, epochs=epochs, batch_size=batch_size)
    model.save('models/' + name + '.keras')