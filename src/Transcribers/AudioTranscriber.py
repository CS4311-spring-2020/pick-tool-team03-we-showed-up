#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:13:38 2020

@author: dgarciaher
"""
import speech_recognition as sr
import os
#import glob

#file_list = []
#for filename in glob.glob('/home/dgarciaher/pick-splunk-implementation/tutorialdata/www2/*.wav'): #assuming gif
    

class AudioRecognition:
    
    def audio_transcribe (folder_path, new_path, filename):
        recognizer = sr.Recognizer()     # selects sphinx library as it is the one that works offline
        
        file_path = os.path.join(folder_path, filename)
        
        logFile = sr.AudioFile(file_path)
        
        with logFile as source:
            audio = recognizer.record(source)

        file_name = filename.strip(".wav")
        
        save_path = (new_path + "/" + file_name + ".txt")    
        
        text_file = open(save_path, "w")
            
        text = recognizer.recognize_sphinx(audio)
        
        text_file.write(text)
        text_file.close()

        return file_name + ".txt"

