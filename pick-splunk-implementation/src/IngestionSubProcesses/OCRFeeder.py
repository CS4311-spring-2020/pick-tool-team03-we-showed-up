from PIL import Image
import pytesseract as pt
import os


class ImageFeeder:
    """This class interfaces with the pytesseract OCR transcriber to convert image files into text."""


    def OCR_transcription(folder_path, new_path, f):
        """Transcribes an image file and saves the text file into the new path, returns the path"""

        input_path = os.path.join(folder_path, f)

        image_file = Image.open(input_path)
        image_text = pt.image_to_string(image_file, lang="eng")

        f = f.split(".")[0] + ".txt"
        final_path = os.path.join(new_path, f)
        f_parsed = open(final_path, "w")
        f_parsed.write(image_text)
        f_parsed.close()
        return f

