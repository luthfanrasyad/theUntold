#Change boot script to this file by typing in terminal -> sudo crontab -e and adding this file
#Purple is recording
#Cyan is idle

import board
import neopixel
import RPi.GPIO as GPIO
import time
import digitalio
from ibm_watson import ToneAnalyzerV3
import busio
import json
import wave
import pyaudio
import speech_recognition as sr

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

pixel_pin = board.D18
num_pixels = 49

ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,pixel_order=ORDER)


def record():
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 44100
    chunk = 4096
    record_secs = 5
    dev_index = 2
    wav_output_filename = 'story.wav'
    audio = pyaudio.PyAudio()
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
    print("recording")
    frames = []
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
    
def speech_to_text(filename):
    r = sr.Recognizer()
    file = sr.AudioFile(filename)
    with file as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
        print(text)
        return text
def detect_emotions(text):
    emotions = []
    tone_analysis = tone_analyzer.tone({'text': text},content_type='application/json').get_result()
    for i in tone_analysis['document_tone']['tones']:
        emotions.append((i['tone_name']))  
    return emotions

def change_color(emotions):
    if 'Fear' in emotions:
        pixels.fill((0,255,0))
        pixels.show()
        print("Green")
    elif 'Sadness' in emotions:
        pixels.fill((0,0,255))
        pixels.show()
        print("Blue")
    elif 'Joy' in emotions:
        pixels.fill((255,255,0))
        pixels.show()
        print("Yellow")
    elif 'Anger' in emotions:
        pixels.fill((255,0,0))
        pixels.show()
        print("Red")

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='BCPnn-DtaBVZEcIU75mDen9uvl8KqrCx7LBUGaIGZ2PQ',
    url='https://gateway-syd.watsonplatform.net/tone-analyzer/api'
)

state = False
counter = 2
while True:
    time.sleep(0.1)
    if (GPIO.input(26) == 1):
        for i in range(num_pixels):
            pixels[i] = (2*i,0,2*i)
            pixels.show()
        counter += 1
        record()
        detected = detect_emotions(speech_to_text("story.wav"))
        print(detected)
        change_color(detected)
        time.sleep(2)
    else:
        for i in range(num_pixels):
            pixels[i] = (0,2*i,2*i)
            pixels.show()




   
    
