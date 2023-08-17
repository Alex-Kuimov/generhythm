from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.callbacks import ModelCheckpoint
from collections import Counter
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import pprint


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


def predict(model, x):
    start = np.random.randint(0, len(x) - 1)
    pattern = x[start]
    prediction_output = []

    for note_index in range(64):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction = model.predict(prediction_input)
        predicted_note = np.argmax(prediction)
        prediction_output.append(predicted_note)

        pattern = np.append(pattern, predicted_note)
        pattern = pattern[1:len(pattern)]

    return prediction_output