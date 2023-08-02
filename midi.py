import os
import mido
import numpy as np
from mido import MidiFile, MidiTrack, Message

def get_midi_files(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


# Загрузка MIDI файла и предобработка данных
def load_midi(file_path):
    midi = mido.MidiFile(file_path)
    notes = []
    for msg in midi:
        if msg.type == 'note_on':
            notes.append(msg.note)
    return np.array(notes)