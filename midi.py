import os
from collections import Counter
from mido import MidiFile, MidiTrack, Message, MetaMessage
from datetime import datetime
import mido
from mido import MidiFile, MidiTrack, Message
import pprint
import random

def get_midi_files(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def get_notes(file):
    mid = mido.MidiFile(file)
    notes = []

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                note = 0 if msg.velocity == 0 else msg.note
                notes.append(note)

    return notes


def create_dict_sequences(notes):
    pattern = []
    patterns_dict = {}
    pattern_id = 1

    for note in notes:
        if note != 0:
            pattern.append(note)
        else:
            if pattern:
                pattern_str = ",".join(str(n) for n in pattern)

                if pattern_str not in patterns_dict and len(pattern_str)<=11:
                    patterns_dict[pattern_str] = pattern_id
                    pattern_id += 1
                pattern = []

    return patterns_dict


def save_to_midi(prediction_output, dict_sequences, style, time, deviation):
    output_notes = []
    for predicted_note in prediction_output:
        notes_str = dict_sequences[predicted_note + deviation] if predicted_note + deviation in dict_sequences else \
        dict_sequences[predicted_note]

        notes = notes_str.split(',')

        t = time
        for note in notes:
            velocity = random.randint(50, 60)
            note_on = Message(type='note_on', note=int(note), velocity=velocity, time=t)
            output_notes.append(note_on)
            t = 0

        t = time
        for note in notes:
            note_on = Message(type='note_on', note=int(note), velocity=0, time=t)
            output_notes.append(note_on)
            t = 0

    # meta_tempo =  MetaMessage('set_tempo', tempo=857143, time=0),
    meta_signature = MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0),

    mid = MidiFile()

    # mid.tracks.append(meta_tempo)
    mid.tracks.append(meta_signature)

    mid.tracks.append(output_notes)

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H-%M-%S")

    filename = f"out/{style}-{current_date}_{current_time}.mid"
    mid.save(filename)

    print("Файл сохранен:", filename)

    return filename