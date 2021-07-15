import io

import keyboard
import numpy as np
import torch
torch.set_num_threads(1)
import torchaudio
import matplotlib
import matplotlib.pylab as plt
torchaudio.set_audio_backend("soundfile")
import pyaudio

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True)

(get_speech_ts,
 get_speech_ts_adaptive,
 save_audio,
 read_audio,
 state_generator,
 single_audio_stream,
 collect_chunks) = utils

# Taken from utils_vad.py
def validate(model,
             inputs: torch.Tensor):
    with torch.no_grad():
        outs = model(inputs)
    return outs

# Provided by Alexander Veysov
def int2float(sound):
    abs_max = np.abs(sound).max()
    sound = sound.astype('float32')
    if abs_max > 0:
        sound *= 1/abs_max
    sound = sound.squeeze()  # depends on the use case
    return sound

FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 16000
CHUNK = int(SAMPLE_RATE / 10)

audio = pyaudio.PyAudio()

# Configure how long you want to record the audio
frames_to_record = 20 # frames_to_record * frame_duration_ms = recording duration
frame_duration_ms = 250

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
data = []
voiced_confidences = []

print("Started Recording")
# for i in range(0, frames_to_record):
while True:
    audio_chunk = stream.read(int(SAMPLE_RATE * frame_duration_ms / 1000.0))

    # in case you want to save the audio later
    data.append(audio_chunk)

    audio_int16 = np.frombuffer(audio_chunk, np.int16);

    audio_float32 = int2float(audio_int16)

    # get the confidences and add them to the list to plot them later
    vad_outs = validate(model, torch.from_numpy(audio_float32))
    # only keep the confidence for the speech
    voiced_confidences.append(vad_outs[:, 1])

    if keyboard.is_pressed('s'):
        # print("\n*Done Recording")
        break

print("Stopped the recording")

# plot the confidences for the speech
plt.figure(figsize=(20, 6))
plt.plot(voiced_confidences)
plt.show()