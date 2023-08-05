import numpy as np

def prepare_sequences(notes, dictionary):
    # Преобразование нот в индексы
    indexes = [dictionary.get(str(note)) for note in notes if dictionary.get(str(note)) is not None]

    # Разделение на последовательности
    sequence_length = 50
    sequences = []
    next_note = []
    for i in range(len(indexes) - sequence_length):
        sequences.append(indexes[i:i + sequence_length])
        next_note.append(indexes[i + sequence_length])

    # Преобразование входных и выходных данных в формат для обучения нейронной сети
    x = np.reshape(sequences, (len(sequences), sequence_length, 1))
    # x = x / float(len(dictionary))  # Нормализация значений входных данных
    y = np.eye(len(dictionary))[next_note]

    return x, y