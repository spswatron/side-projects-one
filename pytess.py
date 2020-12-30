import itertools
from cv2 import *
import cv2
import os
import os.path
from os import listdir
from os.path import isfile, join
from termcolor import cprint
from pdf2image.exceptions import PDFPageCountError

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile

"""
The purpose of this program: iterates through each of the mfa pdfs in the specified directory
and scans their contents via OCR into new txt documents
"""


def ocr_core(filename):
    """
    This function handles the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))
    # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


def represents_int(c):
    """
    checks whether the inputted character c is an integer
    """
    try:
        int(c)
        return True
    except ValueError:
        return False


def get_id(pdf_filename: str):
    """
    gets the int id of mfa file
    """
    filename_original = pdf_filename
    pdf_filename = list(itertools.dropwhile(lambda x: not(represents_int(x)), list(pdf_filename)))
    pdf_filename = list(itertools.takewhile(represents_int, pdf_filename))
    ident = ''.join(pdf_filename)
    pdf_filename = filename_original
    return int(ident)


def change_name(pdf_filename: str, extension: str) -> str:
    """
    This function takes the inputted pdf filename and output a filename
    following the proper naming protocol for txts and csvs for the
    MFA project, which would have the inputted extension.
    """
    return "MFA_" + str(get_id(pdf_filename)) + "c_OCR" + "." + extension


def condition_check(file_name: str):
    """
    Checks for whether the file is an mfa pdf that is not in exclude.txt
    """
    if "mfa" == file_name[:3]:
        return ".pdf" in file_name and file_name[:3] == "mfa" and file_name not in exclude_string
    else:
        return False


def process_file(dir_loc, specific_file):
    """
    Converts specified pdf to images, then scans each image and appends it to a txt file.
    Prints messages based on progress.
    """

    with tempfile.TemporaryDirectory() as path:
        try:
            i = 0
            cprint('Begin processing ' + specific_file + '...', 'blue')
            images = convert_from_path(dir_loc + "/" + specific_file, output_folder=path)
            txt_path = dir_loc + "/" + change_name(specific_file, "txt")
            if os.path.isfile(txt_path):
                os.remove(txt_path)
            cprint("Writing: " + txt_path + "...", 'magenta')
            for image in images:
                i += 1
                f1 = open(txt_path, "a")
                # the line commented out below is another way to preprocess images before
                # the OCR scan that may be used when necessary.
                # os.system('./textcleaner -g ' + image.filename + ' result.png')
                img = cv2.imread(image.filename)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imwrite("result.png", gray)
                result = pytesseract.image_to_string(Image.open("result.png"),
                                                     lang="chi_tra+chi_sim", config=r'--oem 3 --psm 4')
                f1.write(result)
                cprint("finished page " + str(i))
            cprint('Woohoo!! Finished processing ' + specific_file, 'green')
        except PDFPageCountError:
            cprint("Error with " + specific_file + '.\n' +
                   "It may be a good idea to check if your inputted filenames are correct", 'red')


# Iterates through each mfa pdf file in the specified directory to scan via ocr
directory = r"/Volumes/TOSHIBA EXT/Foreign Minstry Documents/Batch 13 - Unprocessed"
cprint("Scanning the files in " + directory + ':', 'blue')
files = [f for f in listdir(directory) if isfile(join(directory, f))]
files = list(filter(condition_check, files))
files.sort(key=get_id)

for file in files:
    process_file(directory, file)