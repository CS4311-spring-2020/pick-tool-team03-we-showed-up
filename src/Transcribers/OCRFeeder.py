from PIL import Image
import pytesseract
import argparse
import cv2
import os

#PyTesseract uses Pillow to import the necessary packages needed for transcribing image files. The Image class in PIL
# loads the input from disk in PIL format, required for PyTesseract.

f_parser = argparse.ArgumentParser() # Initialize setup for parsing imported file
f_parser.add_argument("-i", "--image", required=True, help="new_path")
f_args = vars(f_parser.parse_args())