import keyboard

import pyaudio
import wave
import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np

from moviepy.editor import *

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

print("* recording")

frames = []

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

while True:
    data = stream.read(CHUNK)
    frames.append(data)
    if keyboard.is_pressed('s'):
        # print("\n*Done Recording")
        break


print("\n* done recording")
# print(type(data))


wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

path = 'output.wav'
        # path = 'sample.wav' #파일 업로드 시 사용
sample_rate = 16000

x = librosa.load(path, sample_rate)[0]
S = librosa.feature.melspectrogram(x, sr=sample_rate, n_mels=128)
log_S = librosa.power_to_db(S, ref=np.max)
mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=1)
# print(mfcc)
delta2_mfcc = librosa.feature.delta(mfcc, order=2)
arr = mfcc

# print(type(arr))
print(arr[0])

# print(delta2_mfcc)
len = librosa.get_duration(x)
print(type(x), type(S), type(log_S), type(mfcc), type(len))
import math

# print(x)
# print(S)
# print(delta2_mfcc)
silence = np.count_nonzero(abs(delta2_mfcc) < 10)
size = delta2_mfcc.size

# print(np.count_nonzero(delta2_mfcc))
print("\ntotal length : ", len, "(sec)")
print("time of silence : ", silence, "(frame)")
print("total frame : ", size)
print("speaking rate : ", 100 - silence / size * 100, "%")

plt.figure(figsize=(12, 1))
librosa.display.specshow(delta2_mfcc, x_axis='time')
# plt.ylabel('MFCC coeffs')
# plt.xlabel('Time')
# plt.title('MFCC')
plt.colorbar()
plt.tight_layout()
plt.savefig('result.png',bbox_inches='tight')
plt.show()
