from tensorflow.keras.models import load_model
from prepare import get_notes_from_midi, reindex_dict, create_unique_id_dict, replace_notes_with_ids, create_dict, prepare_sequences, create_midi_file, get_notes
from network import predict
from datetime import datetime


def generate(count, digital_dict, note_dict, x, data_name):
    model = load_model('models/'+data_name+'.keras')
    digital_dict = {value: key for key, value in digital_dict.items()}
    new_digital_notes = []
    new_notes = []

    for i in range(count):
        prediction_output = predict(model, x)
        digital_notes = get_notes(prediction_output, digital_dict)
        new_digital_notes.append(digital_notes)


    for notes in new_digital_notes:
        for id in notes:
            new_notes.append(note_dict[id])

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H-%M-%S")

    filename = f"out/{data_name}-{current_date}_{current_time}.mid"

    create_midi_file(new_notes, filename)

    return filename


def create_drums(data_name):
    notes = get_notes_from_midi('data/' + data_name + '.mid')
    note_dict = reindex_dict(create_unique_id_dict(notes))

    digital_note = replace_notes_with_ids(notes, note_dict)
    digital_dict = create_dict(digital_note)

    x, y = prepare_sequences(digital_note, digital_dict)

    return generate(1, digital_dict, note_dict,  x, data_name)


def create_files(data_name, count):
    files = []
    for _ in range(count):
        file = create_drums(data_name)
        files.append(file)

    return files


# def testing():
#     data_name = 'funk'
#     count = 5
#     create_files(data_name, count)
#
# testing()