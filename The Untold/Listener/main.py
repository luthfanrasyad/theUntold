import requests
import time
from functions import *
import board
import neopixel
import RPi.GPIO as GPIO
import time
from datetime import datetime
import json
import os

pixel_pin = board.D18
num_pixels = 52
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False,
                    pixel_order=ORDER)

# LISTENER SIDE
# Status List:
# 1. idle = Initial status, when no one is inside the booth
# 2. speaker = When the speaker is currently speaking
# 3. listener = When the speaker has finished speaking, the emotion will
#               be sent to the listener. Listener side will read the emotion
#               and ask for feedback. Speaker side will play a pre-recorded msg
# 4. feedback = When the listener has finished saying feedback, and its uploaded
#               speaker side will play that feedback and some pre-recorded msg.

def updateStatus():
    r = requests.get('http://the-untold.herokuapp.com/status')
    return r.json()[0]['status']

    
def main():
    
    STATUS_LIST = ["idle", "speaker", "listener", "feedback"]
    HEROKU_URL = "http://the-untold.herokuapp.com/status/5cc1ab8dfb6fc0265f2903a3"
    bucket = 'the-untold'
    
    pixels.fill((255,255,255))
    pixels.show()
    status = ''
    flag = 0
    print("status")
    while status == '':
        try:
            status = updateStatus()
        except:
            print('reconnecting')
    while True:
        #Do infinite loop, catch current status each loop
        
        if status == STATUS_LIST[1]:
            status = updateStatus()
            print("LISTENER Speaker currently speaking")
            pixels.fill((244,100,200))
            pixels.show()
            flag = 0
            time.sleep(2)
            # DO nothing?
            
        elif status == STATUS_LIST[2]:
            print("ready to start")
            if flag == 0 and (GPIO.input(26) == 1):
                print("LISTENER Listener currently making a feedback")
                playAudio('sound/voiceover/9.2.wav', 2)
                r = requests.get('http://the-untold.herokuapp.com/status')
                emotion = r.json()[0]['emotion']
                score = r.json()[0]['score']
                print("Speaker is currently feeling {}".format(emotion))
                flag = 1
                
            if flag == 1 and (GPIO.input(26) == 1):
                print("button pressed")
                print(emotion)
                print(score)
                print("CHANGING PIXEL")
                pixels.fill((244,100,0))
                pixels.show()
                filename = str(datetime.now()) + '.wav'
                playAudio('sound/voiceover/11.1.wav')
                flag = 2
            
            #put if button here
            if flag == 2 and (GPIO.input(26) == 1):
                print('button press')
                time.sleep(1)

                record(filename)

                uploadFile(bucket, emotion, filename)
                os.remove(filename)
                playAudio('sound/voiceover/13.1.wav')
                #DO record feedback and upload it
                requests.put(HEROKU_URL, json={
                    "status": STATUS_LIST[3],
                    "emotion": emotion,
                    "filename" : filename
                    })
                status = updateStatus()
                

            time.sleep(2)

        elif status == STATUS_LIST[3]:
            print("LISTENER feedback is being played by the speaker")
            status = updateStatus()
            time.sleep(2)
            #DO nothing?

        else:
            pixels.fill((0,255,0))
            pixels.show()
            print("idling")
            status = updateStatus()
            time.sleep(2)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

main()
