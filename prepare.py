import numpy as np
from tensorflow.keras.utils import to_categorical
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage


def get_notes_from_midi(filename):
    notes = []
    midi = MidiFile(filename)

    for track in midi.tracks:
        for message in track:
            if message.type == 'note_on' or message.type == 'note_off':
                type = message.type
                note = message.note
                velocity = message.velocity
                time = message.time
                notes.append((type, note, velocity, time))

    return notes


def create_midi_file(notes, output_filename, ticks_per_beat=960, tempo=500000):
    midi = MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    midi.tracks.append(track)
    tempo = mido.bpm2tempo(120)

    track.append(MetaMessage('set_tempo', tempo=tempo))

    for items in notes:
        for note in items:
            track.append(Message(note[0], note=note[1], velocity=note[2], time=note[3]))

    midi.save(output_filename)


def create_dict(notes):
    unique_notes = list(set(notes))
    return {note: index for index, note in enumerate(unique_notes)}


def create_unique_id_dict(dataset):
    note_dict = {}
    # result = {}
    unique_set = []
    sequence_id = 0
    time = 0

    for i in range(len(dataset)-1):
        item = dataset[i]
        time += item[3]

        unique_set.append(item)

        if time >= 1900:
            sequence_id += 1
            note_dict[sequence_id] = unique_set
            unique_set = []
            time = 0
            continue

    return note_dict


def replace_notes_with_ids(notes, note_dict):
    id_notes = []
    for note in notes:
        for key, value in note_dict.items():
            if note in value:
                id_notes.append(key)
                break
    return id_notes


def prepare_sequences(notes, note_dict):
    sequence_length = 64
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

    x = np.reshape(sequence_input, (len(sequence_input), sequence_length, 1))
    y = to_categorical(sequence_output, num_classes=len(note_dict))

    return x, y


def reindex_dict(note_dict):
    unique_dict = {}
    i = 1
    for key, value in note_dict.items():
        if value not in unique_dict.values():
            unique_dict[i] = value
            i += 1
    return unique_dict


def get_notes(prediction_output, dict):
    notes = []
    for id in prediction_output:
        notes.append(dict[id])

    return notes