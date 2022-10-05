from scipy.io import wavfile
import numpy as np

def fft_cal(in_fft,I,D,P):
    seg_len=2**P
    resample_len=int(seg_len*I/D)
    out_fft=np.zeros((int(resample_len/2)+1))
    for i in range(int(resample_len/2)+1):
        if(i<min(seg_len/2,resample_len/2)):
            out_fft[i]=in_fft[i]*I/D
        else:
            out_fft[i]=in_fft[int(seg_len/2)]
    return out_fft



def audioresample(wavname,I,D,P):
    rate, audio = wavfile.read(wavname)
    audio=audio/np.max(np.abs(audio))
#segmentation length
    seg_len=2**P
#assume overlap length is seg_len/4
    seg_shift=int(seg_len*0.75)
    seg_num=int(len(audio)/seg_shift)
    resample_shift=int(seg_shift*I/D)
    resample_len=resample_shift*seg_num
    resample_seg=int(seg_len*I/D)
    resample_audio=np.zeros((resample_len))
    for i in range(seg_num-1):
        wav_data=audio[i*seg_shift:i*seg_shift+seg_len]
        in_fft=np.fft.rfft(wav_data)
        resample_fft=fft_cal(in_fft,I,D,P)
        resample_Wav=np.fft.irfft(resample_fft)
        resample_audio[i*resample_shift:i*resample_shift+resample_seg] +=resample_Wav[0:resample_seg]
    return resample_audio

#the samplerate of test wav is 16k
if __name__=='__main__':
    wavname='./test.wav'
    resample_audio=audioresample(wavname,3,1,10)
    resample_audio=resample_audio.astype('float32')
    wavfile.write('./resampleout1.wav',48000,resample_audio)
    resample_audio=audioresample(wavname,1,2,10)
    resample_audio=resample_audio.astype('float32')
    wavfile.write('./resampleout2.wav',8000,resample_audio)
    resample_audio=audioresample(wavname,3,2,10)
    resample_audio=resample_audio.astype('float32')
    wavfile.write('./resampleout3.wav',24000,resample_audio)

