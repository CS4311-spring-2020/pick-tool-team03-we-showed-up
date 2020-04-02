from PIL import Image
import pytesseract as pt
import argparse
import difflib
import os

#PyTesseract uses Pillow to import the necessary packages needed for transcribing image files. The Image class in PIL
# loads the input from disk in PIL format, required for PyTesseract.

#f_parser = argparse.ArgumentParser() # Initialize setup for parsing imported file
#f_parser.add_argument("-i", "--image", required=True, help="new_path")
#f_args = vars(f_parser.parse_args())

class ImageFeeder:
    def OCRTranscription(self, folder_path, new_path, f):
        path = new_path # Source Folder/Directory of raw files
        final_path = new_path # Destination Folder/Directory of transcribed files
        for img in os.listdir(path):
            inputPath = os.path.join(path,img)

            image_file = Image.open(inputPath) #Opens file, pre-transcription
            image_text = pt.image_to_string(image_file, lang ="eng") #Transcribes the image file

            #f_path = os.path.join(final_path,'time_'+ img + ".txt") # Set path to store in specified final_path
            f_parsed = open(filename,"w") # Write to specified path
            f_parsed = write(image_text)
            f_parsed.close() # f_parsed is the new transcrbed file


    if __name__ == "__main__":
        pass

