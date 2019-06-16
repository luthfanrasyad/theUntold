import json
import wave
import pyaudio
import boto3
import time
import os
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)


form_1 = pyaudio.paInt16
chans = 1
samp_rate = 44100
chunk = 4096
record_secs = 5
dev_index = 2
wav_output_filename = 'test.wav'
audio = pyaudio.PyAudio()
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                input_device_index = dev_index,input = True, \
                frames_per_buffer=chunk)
print("recording")
frames = []
flag = True

#while flag:
#    data = stream.read(chunk)
#    frames.append(data)
#    if GPIO.input(26) == 1:
#        flag = False

for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)        

print("finished recording")
stream.stop_stream()
stream.close()
audio.terminate()

wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()
