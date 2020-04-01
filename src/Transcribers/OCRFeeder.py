from PIL import Image
import pytesseract as pt
import argparse
import os

from IngestionFunctionality import new_path

#PyTesseract uses Pillow to import the necessary packages needed for transcribing image files. The Image class in PIL
# loads the input from disk in PIL format, required for PyTesseract.

f_parser = argparse.ArgumentParser() # Initialize setup for parsing imported file
f_parser.add_argument("-i", "--image", required=True, help="new_path")
f_args = vars(f_parser.parse_args())

path = new_path # Source Folder/Directory of raw files

final_path = new_path # Destination Folder/Directory of transcribed files
for img in os.listdir(path):
    inputPath = os.path.join(path,img)

    image_file = Image.open(inputPath)
    image_text = pt.image_to_string(image_file, lang ="eng")