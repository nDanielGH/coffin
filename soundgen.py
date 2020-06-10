import os
import numpy as np
from scipy import signal
from scipy.io import wavfile


sample_rate = 44100
freq_gen = lambda base, length: [base * (2 ** i) for i in range(length)]

note_freqs = {
    'C': freq_gen(16.35, 9),
    'C#': freq_gen(17.32, 9),
    'D': freq_gen(18.35, 9),
    'D#': freq_gen(19.45, 9),
    'E': freq_gen(20.60, 9),
    'F': freq_gen(21.83, 9),
    'F#': freq_gen(23.12, 9),
    'G': freq_gen(24.50, 9),
    'G#': freq_gen(25.96, 9),
    'A': freq_gen(27.50, 9),
    'A#': freq_gen(29.14, 9),
    'B': freq_gen(30.87, 9),
    'S': freq_gen(0, 9),        # stop
}

def tone(f, t, sr=sample_rate):
    samples = np.linspace(0, t, int(t * sr), endpoint=False)
    signal = np.int8((2**7 - 1) * np.sin(2 * np.pi * f * samples))
    return signal

def generate_sequence(notes, octaves, times):
    assert len(notes) == len(octaves) == len(times)
    return np.concatenate(
        [tone(note_freqs[note][octave], time)
         for note, octave, time in zip(notes, octaves, times)])


def coffin():
    notes_prologue = [
        'B', 'A', 'G#', 'E'
    ]

    octaves_prologue = [
        4, 4, 4, 4
    ]

    times_prologue = [
        4, 4, 4, 4
    ]

    notes_chorus = [
        'F#', 'F#', 'C#', 'B',
        'A', 'G#', 'G#', 'G#',
        'B', 'A', 'G#', 'F#',
        'F#', 'A', 'G#', 'A',
        'G#', 'A', 'F#', 'F#',
        'A', 'G#', 'A', 'G#',
        'A'
    ]

    octaves_chorus = [
        4, 4, 5, 4,
        4, 4, 4, 4,
        4, 4, 4, 4,
        4, 5, 5, 5,
        5, 5, 4, 4,
        5, 5, 5, 5,
        5
    ]

    times_chorus = [
        8, 4, 4, 8,
        8, 8, 4, 4,
        8, 4, 4, 8,
        4, 4, 4, 4,
        4, 4, 8, 4,
        4, 4, 4, 4,
        4
    ]

    notes_epilogue = [
        'A', 'A', 'A', 'A',
        'C#', 'C#', 'C#', 'C#',
        'B', 'B', 'B', 'B',
        'E', 'E', 'E', 'E',
        'F#', 'F#', 'F#', 'F#',
        'F#', 'F#', 'F#', 'F#',
        'F#', 'F#', 'F#', 'F#'
    ]

    octaves_epilogue = [
        4, 4, 4, 4,
        5, 5, 5, 5,
        4, 4, 4, 4,
        5, 5, 5, 5,
        5, 5, 5, 5,
        5, 5, 5, 5,
        5, 5, 5, 5,
    ]

    times_epilogue = [
        4, 4, 4, 4,
        4, 4, 4, 4,
        4, 4, 4, 4,
        4, 4, 4, 4,
        4, 4, 4, 4,
        4, 4, 4, 4,
        4, 4, 4, 4,
    ]

    notes = notes_prologue + 3 * notes_chorus + notes_epilogue
    octaves = octaves_prologue + 3 * octaves_chorus + octaves_epilogue
    times = times_prologue + 3 * times_chorus + times_epilogue

    times = [t / 18 for t in times]  # speed up

    return notes, octaves, times


wavfile.write('coffin.wav', sample_rate, generate_sequence(*coffin()))
os.system('paplay' + ' coffin.wav')

