import time
import numpy as np
import sounddevice as sd
import tty
import termios
import sys

fs = 44100

sd.default.samplerate = fs
sd.default.channels = 1

for i in range(3):
    print(3 - i)
    time.sleep(0.5)

duration = 0.5
arr = sd.rec(int(duration * fs))
time.sleep(duration)

orig_settings = termios.tcgetattr(sys.stdin)

tty.setraw(sys.stdin)
x = 0

while x != chr(27):
    x = sys.stdin.read(1)[0]
    if x == 'a':
        sd.play(arr)
        time.sleep(duration)
