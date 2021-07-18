import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np
import moviepy.editor as mp

#https://stackoverflow.com/questions/65065501/trim-audio-file-using-python-ffmpeg
#https://stackoverflow.com/questions/55550116/saving-audio-from-mp4-as-wav-file-using-moviepy-audiofile

# mp.VideoFileClip(r"WJ_test.mp4").subclip(0,300).audio.write_audiofile("sample.wav")

# import subprocess
#
# command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format("WJ_test.mp4", "sample.wav")
# subprocess.call(command, shell=True)
# mp.AudioFileClip('SampleAudio2.wav').subclip(0,120).write_audiofile("temp.wav")

# print(type(mp.AudioFileClip('SampleAudio2.wav').subclip(0,120)))

import ffmpeg  

audio_input = ffmpeg.input('SampleAudio2.wav')
audio_cut = audio_input.audio.filter('atrim', duration=150)
audio_output = ffmpeg.output(audio_cut, 'out.mp3')
print(type(audio_cut), type(audio_output))
ffmpeg.run(audio_output)

# path = 'temp.wav'
path = 'SampleAudio2.wav'
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
print(size, silence,"\n", rate, "%", '\n')



speakIndex = np.where(abs(delta2_mfcc)>5)[1]

secIndex = speakIndex*len/size
secIndexUni = np.unique(secIndex.astype(int))
print(speakIndex)
print(np.unique(secIndex.astype(int)), '\n')
# print(secIndexUni[0], secIndexUni[2], secIndexUni[3], secIndexUni[4], secIndexUni[5])

toggle = True

# for i in speakIndex:
#     if i-6&i-5&i-4&i-3&i-2&i-1&i&i+1&i+2&i+3&i+4&i+5&i+6 in speakIndex :
#         if Toggle == True :
#             speakCount+=1
#             print(i, "frame , ",i*len/size, "")
#             Toggle = False
#     else :
#         Toggle = True

temp=0
speakCount=0
arrLen = secIndexUni.size

speakLen = 0
for j in secIndexUni:
    if (j-2 in secIndexUni) & (j-1 in secIndexUni) & (j in secIndexUni):
        if temp == 0:
            speakCount=speakCount+1
            temp = 1
            print(j)
        else:
            print(" ")
            speakLen+=1
    else :
        temp = 0

speakLen = speakLen + speakCount*3

print("Number he/she has spoken is : " , speakCount, "times")
print("Time he/she has spoken is : " , speakLen, "sec")

# print(delta2_mfcc[0][8111])

# y = librosa.load(path,sample_rate)

plt.figure(figsize=(9, 3))
# librosa.display.waveplot(log_S)
print(delta2_mfcc[0][0:10])
plt.plot(delta2_mfcc[0])
# print(type(x), type(delta2_mfcc))

# librosa.display.specshow(delta2_mfcc, x_axis='time')

# plt.ylabel('MFCC coeffs')
# plt.xlabel('Time')
# plt.title('MFCC')
# plt.colorbar()
# plt.tight_layout()
# plt.savefig("result.png")
plt.show()