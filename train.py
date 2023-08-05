from midi import get_midi_files, get_notes, create_dict_sequences
from prepare import prepare_sequences
from network import create_network, train

data_name = 'pop'

midi_files = get_midi_files('data/'+data_name)

notes = []
for file in midi_files:
    notes += get_notes(file)

dict_sequences = create_dict_sequences(notes)

print(dict_sequences)

x, y = prepare_sequences(notes, dict_sequences)

num_features = len(set(dict_sequences))
input_dim = 1

model = create_network(input_dim, num_features)
train(model, x, y, epochs=50, batch_size=64, name=data_name)