from tensorflow.keras.models import load_model
from network import generate
from midi import get_midi_files, get_notes, create_dict_sequences
from prepare import prepare_sequences

def create_drums(data_name, deviation, time):
    model = load_model('models/' + data_name + '.keras')
    midi_files = get_midi_files('data/' + data_name)

    notes = []
    for file in midi_files:
        notes += get_notes(file)

    dict_sequences = create_dict_sequences(notes)

    x, y = prepare_sequences(notes, dict_sequences)

    dict = {value: key for key, value in dict_sequences.items()}

    generate(model, x, dict, data_name, deviation, time)

data_name = 'pop'
count = 10
deviation = 1
time = 110

for _ in range(count):
    create_drums(data_name, deviation, time)