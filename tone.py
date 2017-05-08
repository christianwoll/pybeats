import time
import numpy as np
import sounddevice as sd

# Dictionary:
# fs - F-something per second
# wf - waveform

fs = 44100

sd.default.samplerate = fs 
sd.default.channels = 1

class Wave:
    sine = lambda x: np.sin(2*np.pi * x)

    def __init__(self, freq=None, amp=0.5, shape=None):
        self.freq = freq
        self.amp = amp
        self.shape = shape if not shape is None else self.sine

    def array(self, duration):
        if self.freq is None: return np.zeros(int(duration * fs))

        period = int(fs / self.freq)
        single = np.fromfunction(lambda i: self.amp * self.shape(i/period), (period,))
        wf = np.tile(single, int(self.freq * duration + 1))

        return wf 
        
class Song:
    def __init__(self, tempo=0.125, base_freq=440):
        self.tempo = tempo 
        self.key = [base_freq*2**(n/12) for n in range(12)]
        self.arr = np.array([0.0])  

    def play(self):
        sd.play(self.arr)
        time.sleep(len(self.arr) / fs)
        sd.stop()

    def add(self, seq, beat, amp=0.5, shape=Wave.sine, octave=0):
        seq = [None if n == '' else n + 12*octave for n in seq]

        freqs = [None if n is None else self.key[n%12]*2**(n//12) for n in seq]
        waves = [Wave(f, amp, shape) for f in freqs]
        newarr = np.concatenate([wave.array(self.tempo) for wave in waves])

        offset = int(beat * self.tempo * fs)
        newarr = np.concatenate((np.zeros(offset), newarr))

        if len(self.arr) < len(newarr):
            self.arr = np.concatenate((self.arr, np.zeros(len(newarr) - len(self.arr))))
        if len(newarr) < len(self.arr):
            newarr = np.concatenate((newarr, np.zeros(len(self.arr) - len(newarr))))
        
        self.arr = (self.arr + newarr)
                    
    def loop(self, num):
        self.arr = np.tile(self.arr, num)

song = Song(0.2, 261.625)

melody = [6,8,6,10,8,10,6,8]+[5,6,5,10,6,10,5,6]+[3,6,3,10,3,10,5,3]+[11,10,11,6,10,11,6,11]
song.add(melody, 0)

bass = [6,'',6,'',6,'',6,'']+[5,'',5,'',5,'',5,'']+[3,'',3,'',3,'',3,'']+[-1,'',-1,'',-1,'',-1]
song.add(bass, 0, 0.2, octave=-2)
song.add(bass, 1, 0.2, octave=-1)

song.loop(2)
song.play()
