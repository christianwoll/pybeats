import time
import numpy as np
import sounddevice as sd

fs = 44100

sd.default.samplerate = fs 
sd.default.channels = 1

class Wave:
    # Functions go from -1 to 1
    sine = lambda x: np.sin(2*np.pi * x)
    bit8 = lambda x: np.round(np.sin(2*np.pi * x) * 4) / 4

    def __init__(self, freq, amp, shape):
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
    roct = 2
    steps = 12

    def __init__(self, tempo, fbase):
        self.tempo = tempo 
        self.key = [fbase * self.roct**(n/self.steps) for n in range(self.steps)]
        self.arr = np.array([0.0])  

    def play(self):
        sd.play(self.arr)
        time.sleep(len(self.arr) / fs)
        sd.stop()

    def add(self, seq, beat, amp=0.5, shape=Wave.sine, octave=0):
        seq = [None if n == '' else n + self.steps * octave for n in seq]

        freqs = [None if n is None else self.key[n%self.steps] * self.roct**(n//self.steps) for n in seq]
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

roct = 2
steps = 12

tempo = 0.2
fbase = 200

key = [fbase * roct**(n/steps) for n in range(steps)]



seq = [6,8,6,10,8,10,6,8]+[5,6,5,10,6,10,5,6]+[3,6,3,10,3,10,5,3]+[11,10,11,6,10,11,6,11]

seq = [None if n == '' else n for n in seq]
freqs = [None if n is None else key[n%steps] * roct**(n//steps) for n in seq]
waves = [Wave(f, 0.5, Wave.sine) for f in freqs]
arr = np.concatenate([wave.array(tempo) for wave in waves])

sd.play(arr)
time.sleep(len(arr) / fs)
sd.stop()
