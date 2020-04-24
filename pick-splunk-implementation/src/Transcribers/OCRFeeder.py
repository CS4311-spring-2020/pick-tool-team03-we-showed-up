from PIL import Image
import pytesseract as pt
import argparse
import difflib
import os

#PyTesseract uses Pillow to import the necessary packages needed for transcribing image files. The Image class in PIL
# loads the input from disk in PIL format, required for PyTesseract.


class ImageFeeder:

    def OCR_transcription(folder_path, new_path, f):

        input_path = os.path.join(folder_path, f)

        image_file = Image.open(input_path)  # Opens file, pre-transcription
        image_text = pt.image_to_string(image_file, lang="eng")  # Transcribes the image file

        f = f.split(".")[0] + ".txt"
        final_path = os.path.join(new_path, f)
        f_parsed = open(final_path, "w")  # Write to specified path
        f_parsed.write(image_text)
        f_parsed.close()  # f_parsed is the new transcrbed file
        # return the final path of the file
        return f

