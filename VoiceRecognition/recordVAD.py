import io
import numpy as np
import torch
torch.set_num_threads(1)
import torchaudio
import matplotlib
import matplotlib.pylab as plt
torchaudio.set_audio_backend("soundfile")
import pyaudio
import wave

torch.backends.quantized.engine = 'qnnpack'

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

voiced_confidences = []

def read_wav(path:str):
    with wave.open('sample.wav', mode='rb') as wavread:
        fs = wavread.getframerate()
        fr = wavread.getnframes()
        start = 0
        duration = (fr/fs)
        wavread.setpos(start)
        wav_bytes = wavread.readframes(duration)

        wav_array = np.frombuffer(wav_bytes, dtype=np.int16)
        return wav_array

audio_chunk = read_wav('sample.wav')

for i in range (0,10):
    audio_int16 = np.frombuffer(audio_chunk, np.int16)

    audio_float32 = int2float(audio_int16)
    
    # get the confidences and add them to the list to plot them later
    vad_outs = validate(model, torch.from_numpy(audio_float32))
    # only keep the confidence for the speech
    voiced_confidences.append(vad_outs[:,1])
    
print(voiced_confidences)
# plot the confidences for the speech
plt.figure(figsize=(20,6))
plt.plot(voiced_confidences)
plt.show()