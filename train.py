from prepare import get_notes_from_midi, reindex_dict, create_unique_id_dict, replace_notes_with_ids, create_dict, prepare_sequences
from network import create_network, train

data_name = 'rock'
notes = get_notes_from_midi('data/'+data_name+'.mid')
note_dict = reindex_dict(create_unique_id_dict(notes))

digital_note = replace_notes_with_ids(notes, note_dict)
digital_dict = create_dict(digital_note)

x,y = prepare_sequences(digital_note, digital_dict)

num_features = len(set(digital_dict))
input_dim = 1

model = create_network(input_dim, num_features)
train(model, x, y, epochs=50, batch_size=64, name=data_name)
