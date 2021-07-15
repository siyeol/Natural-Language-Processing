import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np
import moviepy.editor as mp

# mp.VideoFileClip(r"WJ_test.mp4").subclip(0,300).audio.write_audiofile("sample.wav")

# import subprocess
#
# command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format("WJ_test.mp4", "sample.wav")
# subprocess.call(command, shell=True)

path = 'sample.wav'
sample_rate=16000

x = librosa.load(path,sample_rate)[0]
S = librosa.feature.melspectrogram(x, sr=sample_rate, n_mels=128)
log_S = librosa.power_to_db(S, ref=np.max)
mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=1)

delta2_mfcc = librosa.feature.delta(mfcc, order=2)

len = librosa.get_duration(x)
silence = np.count_nonzero(abs(delta2_mfcc) < 2)
size = delta2_mfcc.size
rate = 100 - silence / size * 100
print(size, silence,"\n", rate, "%")

y = librosa.load(path,sample_rate)

plt.figure(figsize=(12, 1))
librosa.display.waveplot(y,sr=sample_rate, x_axis="time")
# plt.ylabel('MFCC coeffs')
# plt.xlabel('Time')
# plt.title('MFCC')
plt.colorbar()
plt.tight_layout()
plt.show()