import board
import digitalio
from ibm_watson import ToneAnalyzerV3
import busio
import neopixel
import time
import json
import wave
import pyaudio
import speech_recognition as sr



emotions = []
num_pixels = 49
pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=ORDER)


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
 
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)



tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='BCPnn-DtaBVZEcIU75mDen9uvl8KqrCx7LBUGaIGZ2PQ',
    url='https://gateway-syd.watsonplatform.net/tone-analyzer/api'
)



  
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 5 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("recording")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()

r = sr.Recognizer()
harvard = sr.AudioFile("test1.wav")

with harvard as source:
    audio = r.record(source)
    text = r.recognize_google(audio)
    print(text)
    


tone_analysis = tone_analyzer.tone(
    {'text': text},
    content_type='application/json'
).get_result()

for i in tone_analysis['document_tone']['tones']:
    emotions.append((i['tone_name']))
print(emotions)


if 'Fear' in emotions:
    pixels.fill((0,255,0))
    pixels.show()
elif 'Sadness' in emotions:
    pixels.fill((0,0,255))
    pixels.show()
elif 'Joy' in emotions:
    pixels.fill((255,255,0))
    pixels.show()
elif 'Anger' in emotions:
    pixels.fill((255,0,0))
    pixels.show()




