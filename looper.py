import time
import numpy as np
import sounddevice as sd
import tty
import termios
import sys

fs = 44100

sd.default.samplerate = fs
sd.default.channels = 1

beat = 0.25

for i in range(5):
    for j in range(4):
        print(str(j+1) + '' if j else '--------' + str(5-i))
        time.sleep(beat)

count = 16
duration = beat * count
arr = sd.rec(int(duration * fs))

print('GO')
for i in range(count // 4):
    for j in range(4):
        print(str(j+1) + '' if j else '--------' + str(i+1))
        time.sleep(beat)


orig_settings = termios.tcgetattr(sys.stdin)

tty.setraw(sys.stdin)
x = 0
newarr = None

while True:
    x = sys.stdin.read(1)[0]
    print('input=',x)

    if x == 'r':
        newarr = sd.rec(int(duration * fs))
    else:
        sd.play(arr)

    print('GO')
    for i in range(count // 4):
        for j in range(4):
            print(str(j+1) + '' if j else '--------' + str(i+1))
            time.sleep(beat)

    if not newarr is None:
        arr = arr + newarr
