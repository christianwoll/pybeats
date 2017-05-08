import time
import numpy as np
import sounddevice as sd

# Dictionary:
# fs - F-something per second
# wf - waveform

fs = 44100
sd.default.samplerate = fs 
sd.default.channels = 1

def tone(freq, duration):
    period = int(fs / freq)
    wave = [n / period for n in range(period)]
    tone = wave * int(freq * duration + 1)
    return tone[:int(duration * fs)]
    
def play(wf):
    sd.play(wf)
    time.sleep(len(wf) / fs)
    sd.stop()

key = [261.625*2**(n/12) for n in range(12)]

def seq(notes, beat):
    sound = []
    for n in notes: sound += tone(key[n%12]*2**(n//12), beat)
    return sound

def chord(notes, beat):
    return merge(*[seq([n], beat) for n in notes])

def merge(*wf_arr):
    M = max([len(wf) for wf in wf_arr])
    WF_arr = [wf + [0.0] * (M - len(wf)) for wf in wf_arr]
    return [np.mean(v) for v in zip(*WF_arr)]
    
beat = 0.4

har = seq([10,7]*4 + [9,5]*4 + [7,4]*4 + [5,2]*4, beat)
har += seq([10,7]*4 + [14,9]*4 + [12,7]*4 + [10,5]*4, beat)

play(har)
