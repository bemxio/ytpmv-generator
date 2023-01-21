from pydub.effects import speedup as speed_up
from audio_effects import speed_down

from pydub import AudioSegment
import mido

def get_tempo(file: mido.MidiFile) -> int:
    for message in file:
        if message.type == "set_tempo":
            return message.tempo
    
    return 500000

def get_longest_note(track: mido.MidiTrack) -> float:
    notes = {}
    time = 0
    lengths = []

    for message in track:
        time += message.time

        if message.type not in ("note_on", "note_off"):
            continue
    
        if message.type == "note_on" and message.velocity > 0:
            notes[message.note] = time
            continue

        position = notes.get(message.note, 0)
        length = time - position

        lengths.append(length)
        
        if message.note in notes:
            notes.pop(message.note)
    
    return max(lengths) if len(lengths) != 0 else 0

def speed_change(segment: AudioSegment, speed: float = 1.0):
    if speed >= 1.0:
        return speed_up(segment, speed, chunk_size=25)
    else:
        return speed_down(segment, speed)

def pitch_change(segment: AudioSegment, note: int, root_note: int = 72) -> AudioSegment:
    octaves = (note - root_note) / 12

    modified = segment._spawn(segment.raw_data, overrides={
        "frame_rate": int(segment.frame_rate * (2.0 ** octaves))
    })

    return modified.set_frame_rate(segment.frame_rate)

song = AudioSegment.from_wav("song.wav")
baseline = mido.MidiFile("baseline.mid")

print("Select the MIDI tracks to be used as a baseline:")

for index, track in enumerate(baseline.tracks, start=1):
    print(f"#{index}: \"{track.name}\"")

print("\nType out your choice by seperating the choices with a **comma**,")
print("ex. `3,2,4,6`\n")

choices = input("Your answer: ")
choices = [int(index) - 1 for index in choices.split(",")]

if not choices:
    choices = range(len(baseline.tracks))
 
tracks = [baseline.tracks[index] for index in choices]

ticks_per_beat = baseline.ticks_per_beat
tempo = get_tempo(baseline)

samples = [
    # the AudioSegment, root note
    (AudioSegment.from_wav(f"samples/sample1.wav"), 79 - 12),
    (AudioSegment.from_wav(f"samples/sample2.wav"), 77 - 12),
    (AudioSegment.from_wav(f"samples/sample3.wav"), 81 - 12)
]

for track in tracks:
    longest = get_longest_note(track) / len(samples)
    notes = {}
    time = 0

    for message in track:
        time += message.time

        if message.type not in ("note_on", "note_off"):
            continue
    
        if message.type == "note_on" and message.velocity > 0:
            notes[message.note] = time
            continue

        position = notes.get(message.note, 0)

        length = time - position
        seconds = mido.tick2second(length, ticks_per_beat, tempo)

        if seconds <= longest:
            sample, root_note = samples[0]
        elif seconds <= longest * 2:
            sample, root_note = samples[1]
        else:
            sample, root_note = samples[2]

        multiplier = len(sample) / (seconds * 1000)

        sample = pitch_change(sample, message.note, root_note=root_note - 12)
        sample = speed_change(sample, multiplier)

        position = int(mido.tick2second(position, ticks_per_beat, tempo) * 1000)

        song = song.overlay(sample, position=position)

        print(f"Added note {message.note} at position {position} to the song")
        
        if message.note in notes:
            notes.pop(message.note)

song.export("final.wav", format="wav")
