from tensorflow.keras.models import load_model
from network import generate
from midi import get_midi_files, get_notes, create_dict_sequences
from prepare import prepare_sequences

def create_drums(data_name, deviation, time, note_count):
    model = load_model('models/' + data_name + '.keras')
    midi_files = get_midi_files('data/' + data_name)

    notes = []
    for file in midi_files:
        notes += get_notes(file)

    dict_sequences = create_dict_sequences(notes)

    x, y = prepare_sequences(notes, dict_sequences)

    dict = {value: key for key, value in dict_sequences.items()}

    return generate(model, x, dict, data_name, deviation, time, note_count)


def create_files(data_name, count, deviation, time, note_count):
    files = []
    for _ in range(count):
        file = create_drums(data_name, deviation, time, note_count)
        files.append(file)

    return files


# data_name = 'rock'
# count = 2
# deviation = 0
# time = 90
# note_count = 42
#
# create_files(data_name, count, deviation, time, note_count)