import time
import numpy as np
import sounddevice as sd

# Dictionary:
# fs - F-something per second
# wf - waveform

fs = 44100
sd.default.samplerate = fs 
sd.default.channels = 1

def wave(freq, duration, volume=1, form=None, decay=1):
    if form is None: form = lambda x: np.sin(2*np.pi * x)
    if freq is None: return np.zeros(int(duration * fs))

    period = int(fs / freq)
    single = np.fromfunction(lambda i: form(i/period), (period,))
    tone = np.tile(single, int(freq * duration + 1))

    return tone
    
def play(wf):
    sd.play(wf)
    time.sleep(len(wf) / fs)
    sd.stop()

key = [261.625*2**(n/12) for n in range(12)]

def seq(notes, beat, form=None):
    freqs = [None if n is None else key[n%12]*2**(n//12) for n in notes]
    return np.concatenate([wave(f, beat, form) for f in freqs])

def chord(notes, beat):
    return merge(*[seq([n], beat) for n in notes])

def merge(*wf_arr):
    M = max([len(wf) for wf in wf_arr])
    WF_arr = [wf + [0.0] * (M - len(wf)) for wf in wf_arr]
    return [np.mean(v) for v in zip(*WF_arr)]
    
beat = 0.2
song = np.array([])

song = np.concatenate((song, seq([6,8,None,10,8,None,6,8], beat)))
song = np.concatenate((song, seq([5,6,None,10,6,None,5,6], beat)))
song = np.concatenate((song, seq([3,6,None,10,3,None,5,3], beat)))
song = np.concatenate((song, seq([11,10,None,6,10,None,6,11], beat)))
song = np.tile(song, 4)
play(song)
