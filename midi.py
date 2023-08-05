import os
import mido
from mido import MidiFile, MidiTrack, Message
import pprint

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

                if pattern_str not in patterns_dict:
                    patterns_dict[pattern_str] = pattern_id
                    pattern_id += 1
                pattern = []

    return patterns_dict