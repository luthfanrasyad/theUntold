#!/bin/env python
import json
from watson_developer_cloud import ToneAnalyzerV3

text = "I am very sad"


tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='BCPnn-DtaBVZEcIU75mDen9uvl8KqrCx7LBUGaIGZ2PQ',
    url='https://gateway-syd.watsonplatform.net/tone-analyzer/api')

def detect_emotions(text):
    emotions = {}
    tone_analysis = tone_analyzer.tone({'text': text},content_type='application/json').get_result()
    for i in tone_analysis['document_tone']['tones']:
       emotions[i['tone_name']] =  i['score']
    return emotions
   
def change_color(emotions):

   if 'Fear' in emotions:
      #pixels.fill((0,255,0))
      #pixels.show()
      intensity = (emotions["Fear"]*255)
      print("Green" , intensity) 
   elif 'Sadness' in emotions:
      #pixels.fill((0,0,255))
      #pixels.show()
      intensity = (emotions["Sadness"]*255)
      print("Blue",intensity)

   elif 'Joy' in emotions:
      #pixels.fill((255,255,0))
      #pixels.show()
      intensity = (emotions["Joy"]*255)
      print("Yellow")
   elif 'Anger' in emotions:
      #pixels.fill((255,0,0))
      #pixels.show()
      intensity = (emotions["Anger"]*255)
      print("Red",intensity)

change_color(detect_emotions(text))


