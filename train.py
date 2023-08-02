from prepare import prepare_sequences, get_midi_files, convert_midi_to_digital_format, create_note_dict
from network import create_network, train

# Загрузка MIDI файлов и подготовка данных
midi_files = get_midi_files('data/rock') # Список ваших MIDI файлов

notes = []
for file in midi_files:
    notes += convert_midi_to_digital_format(file)

note_dict = create_note_dict(notes)
x, y = prepare_sequences(notes, note_dict)

n_vocab = len(set(notes))
input_dim = 1

model = create_network()
train(model, x, y, epochs=50, batch_size=64)