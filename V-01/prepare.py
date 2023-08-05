import mido
import numpy as np
import os
from keras.models import load_model
from tensorflow.keras.utils import to_categorical
from network import create_network, train
from midi import get_midi_files, load_midi
from mido import MidiFile, MidiTrack, Message
from datetime import datetime
import random
from collections import Counter

def convert_midi_to_digital_format(midi_file):
    try:
        mid = mido.MidiFile(midi_file)
    except FileNotFoundError:
        print("Midi file not found.")
        return

    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000  # default tempo in microseconds per beat

    # Find tempo change events to update the tempo
    for msg in mid:
        if msg.type == 'set_tempo':
            tempo = msg.tempo

    ticks_per_note = 4  # Assumed default value for quarter note

    # Duration calculation based on tick resolution and tempo
    ticks_per_second = ticks_per_beat * (10 ** 6) / tempo
    duration_per_tick = 1 / ticks_per_second

    # Process midi events
    notes_and_chords = []

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                if msg.velocity == 0:
                    note = 1
                else:
                    note = msg.note

                ticks = int(msg.time)
                duration = duration_per_tick * ticks

                # Convert duration to nearest possible musical note duration
                if duration > 0:
                    note_duration = round(ticks_per_note * duration)
                    duration = note_duration / ticks_per_note

                notes_and_chords.append((note, duration))

    return notes_and_chords


def prepare_sequences(notes, note_dict):
    sequence_length = 100  # Длина каждой последовательности (можно изменить по вашему усмотрению)
    sequence_input = []
    sequence_output = []

    # Создание словаря индексов для нот
    index_dict = {note: index for index, note in enumerate(note_dict)}

    for i in range(len(notes) - sequence_length):
        sequence_in = notes[i: i + sequence_length]
        sequence_out = notes[i + sequence_length]

        sequence_input.append([index_dict[note] for note in sequence_in])

        if sequence_out in index_dict:
            sequence_output.append(index_dict[sequence_out])

    # Преобразование входных и выходных последовательностей в формат numpy массивов
    x = np.reshape(sequence_input, (len(sequence_input), sequence_length, 1))
    y = to_categorical(sequence_output, num_classes=len(note_dict))

    return x, y


def create_note_dict(notes):
    unique_notes = list(set(notes))
    note_dict = {note: index for index, note in enumerate(unique_notes)}

    return note_dict


def gen_drums(model, note_dict, x, style):
    start = np.random.randint(0, len(x) - 1)
    pattern = x[start]

    prediction_output = []

    for note_index in range(128):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction = model.predict(prediction_input)
        predicted_note = np.argmax(prediction)
        prediction_output.append(predicted_note)
        pattern = np.append(pattern, predicted_note)
        pattern = pattern[1:len(pattern)]

    counted_values = Counter(prediction_output)
    unique_values = len(counted_values)

    print(prediction_output)
    print(unique_values)

    if unique_values < 5:
        gen_drums(model, note_dict, x, style)
    else:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H-%M-%S")

        filename = f"{style}-{current_date}_{current_time}.txt"
        path = os.path.join("out", filename)

        os.makedirs("out", exist_ok=True)

        with open(path, "w") as file:
            for item in prediction_output:
                file.write(str(item) + "\n")

        print("Массив сохранен в файл:", path)

        output_notes = []
        velocity = random.randint(80, 90)

        for predicted_note in prediction_output:
            note = next((k for k, v in note_dict.items() if v == predicted_note), None)

            note_on = Message(type='note_on', note=note[0], velocity=velocity, time=115)
            note_off = Message(type='note_off', note=note[0], velocity=0, time=115)

            if note[0] == 1:
                velocity = random.randint(50, 60)
            else:
                velocity = random.randint(80, 90)

            if note[0] != 1:
                output_notes.append(note_on)
                output_notes.append(note_off)

        mid = MidiFile()
        track = MidiTrack()

        for note in output_notes:
            track.append(note)

        mid.tracks.append(track)

        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H-%M-%S")

        filename = f"out/{style}-{current_date}_{current_time}.mid"
        mid.save(filename)

        print("Файл сохранен:", filename)
        return filename
