#!/bin/env python
import json
import speech_recognition as sr
from watson_developer_cloud import ToneAnalyzerV3

text = 'I dropped my phone in the toilet yesterday'


tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='BCPnn-DtaBVZEcIU75mDen9uvl8KqrCx7LBUGaIGZ2PQ',
    url='https://gateway-syd.watsonplatform.net/tone-analyzer/api'
)

r = sr.Recognizer()

with sr.Microphone() as source:
   print('Speak Anything : ')
   audio = r.listen(source)

   try:
      text = r.recognize_google(audio)
      tone_analysis = tone_analyzer.tone(
    {'text': text},
    'application/json'
).get_result()
      print('You said : {}'.format(text))
      
   except:
      print("Sorry could not recognize your voice")


print(json.dumps(tone_analysis, indent=2))






