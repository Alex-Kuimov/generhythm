from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.callbacks import ModelCheckpoint
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from collections import Counter
from mido import MidiFile, MidiTrack, Message, MetaMessage
import pprint
from datetime import datetime
import random


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


def generate(model, x, dict_sequences, style, deviation, time):
    start = np.random.randint(0, len(x) - 1)
    pattern = x[start]

    prediction_output = []

    for note_index in range(40):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction = model.predict(prediction_input)
        predicted_note = np.argmax(prediction)
        prediction_output.append(predicted_note)
        pattern = np.append(pattern, predicted_note)
        pattern = pattern[1:len(pattern)]

    counted_values = Counter(prediction_output)
    unique_values = len(counted_values)

    if unique_values < 3:
        generate(model, x, dict_sequences, style, deviation, time)
    else:
        output_notes = []
        for predicted_note in prediction_output:
            notes_str = dict_sequences[predicted_note + deviation] if predicted_note + deviation in dict_sequences else dict_sequences[predicted_note]

            notes = notes_str.split(',')

            t = time
            for note in notes:
                velocity = random.randint(50, 60)
                note_on = Message(type='note_on', note=int(note), velocity=velocity, time=t)
                output_notes.append(note_on)
                t = 0

            t = time
            for note in notes:
                velocity = random.randint(50, 60)
                note_on = Message(type='note_on', note=int(note), velocity=0, time=t)
                output_notes.append(note_on)
                t = 0

        meta_tempo =  MetaMessage('set_tempo', tempo=857143, time=0),
        meta_signature = MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0),

        mid = MidiFile()

        mid.tracks.append(meta_tempo)
        mid.tracks.append(meta_signature)

        mid.tracks.append(output_notes)

        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H-%M-%S")

        filename = f"out/{style}-{current_date}_{current_time}.mid"
        mid.save(filename)

        print("Файл сохранен:", filename)
