import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np

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



speakCount =0
speakIndex = np.where(abs(delta2_mfcc)>5)[1]
print(speakIndex.size)

toggle = True

for i in speakIndex:
    if i-3&i-2&i-1&i&i+1&i+2&i+3 in speakIndex :
        if Toggle == True :
            speakCount+=1
            print(i)
            Toggle = False
    else :
        Toggle = True
    
    

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