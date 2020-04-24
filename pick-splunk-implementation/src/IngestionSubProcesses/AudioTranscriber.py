import speech_recognition as sr
import os

class AudioRecognition:
    """This class interfaces with the Sphinx transcriber to transcribe an audio file."""
    

    def audio_transcribe(folder_path, new_path, filename):
        """Transcribes an audio file and saves the text file into the new path."""
        recognizer = sr.Recognizer()
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

