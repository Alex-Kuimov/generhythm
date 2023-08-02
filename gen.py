from keras.models import load_model
from prepare import gen_drums, convert_midi_to_digital_format, get_midi_files, prepare_sequences, create_note_dict

def gen(style, count):
    model = load_model('models/' + style + '.keras')

    midi_files = get_midi_files('data/' + style)  # Список ваших MIDI файлов

    notes = []
    for file in midi_files:
        notes += convert_midi_to_digital_format(file)

    note_dict = create_note_dict(notes)
    x, y = prepare_sequences(notes, note_dict)

    file_names = []
    for _ in range(count):
        drum_file = gen_drums(model, midi_files, notes, note_dict, x, style)
        file_names.append(drum_file)

    return file_names

# styles = ['pop', 'funk', 'post-rock', 'rock', 'soul']
#
# for style in styles:
#     gen(style, 10)

#gen('rock', 10)