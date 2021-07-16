import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np

# mp.VideoFileClip(r"WJ_test.mp4").subclip(0,300).audio.write_audiofile("sample.wav")

# import subprocess
#
# command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format("WJ_test.mp4", "sample.wav")
# subprocess.call(command, shell=True)

path = 'SampleAudio1.wav'
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



speakIndex = np.where(abs(delta2_mfcc)>5)[1]

secIndex = speakIndex*len/size
secIndexUni = np.unique(secIndex.astype(int))
# print(speakIndex)
print(np.unique(secIndex.astype(int)))
# print(secIndexUni[0], secIndexUni[2], secIndexUni[3], secIndexUni[4], secIndexUni[5])

toggle = True

# for i in speakIndex:
#     if i-6&i-5&i-4&i-3&i-2&i-1&i&i+1&i+2&i+3&i+4&i+5&i+6 in speakIndex :
#         if Toggle == True :
#             speakCount+=1
#             print(i, "frame , ",i*len/size, "초")
#             Toggle = False
#     else :
#         Toggle = True

temp=0
speakCount=0
arrLen = secIndexUni.size
for j in secIndexUni:
    if (j-2 in secIndexUni) & (j-1 in secIndexUni) & (j in secIndexUni):
        if temp == 0:
            speakCount=speakCount+1
            temp = 1
            print(j)
    else :
        temp = 0



print("this is the number of speaks" , speakCount)

# print(delta2_mfcc[0][8111])

# y = librosa.load(path,sample_rate)

plt.figure(figsize=(9, 3))
librosa.display.waveplot(x)

# librosa.display.specshow(delta2_mfcc, x_axis='time')

# plt.ylabel('MFCC coeffs')
# plt.xlabel('Time')
# plt.title('MFCC')
# plt.colorbar()
# plt.tight_layout()
plt.show()