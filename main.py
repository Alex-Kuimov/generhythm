from mido import MidiFile, MidiTrack, Message
from prepare import convert_midi_to_digital_format
import random


midi = convert_midi_to_digital_format('data/piano/01/75bpm A.mid');

print(midi)
output_notes = []

for note in midi:

    if note[0] == 'note_on':
        new_note = Message(type=note[0], note=note[1], velocity=note[2], time=note[3])

    if note[0] == 'control_change':
        new_note = Message(type=note[0], control=note[1], value=note[2], time=note[3])

    output_notes.append(new_note)

mid = MidiFile()
track = MidiTrack()

for note in output_notes:
    track.append(note)

mid.tracks.append(track)

mid.save('out/test.mid')