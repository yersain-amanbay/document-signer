from dotenv import load_dotenv
from PIL import Image
import glob
import fitz
import os

load_dotenv()

sign_path = os.getenv("SIGN")
width = os.getenv("SIGN_WIDTH")
height = os.getenv("SIGN_HEIGHT")
position = (width, height)

input_path = os.getenv("INPUT")
output_path = os.getenv("OUTPUT")
tmp_path = os.getenv("TMP_FOLDER")


# Create temp image Folder
try:
    os.mkdir(tmp_path)
except OSError:
    pass


# Delete all files in folder
def clearFolder(folder):
    for filename in glob.glob(folder+"*.*"):
        os.remove(filename)


# Convert PDF to PNG
for filename in glob.glob(input_path+"*.pdf"):
    for page in fitz.open(filename):
        pix = page.get_pixmap(matrix=fitz.Matrix(3.0, 3.0))
        pix.save(tmp_path+filename[len(input_path):-4]+".png")

# Sign PNG and convert it to PDF
for filename in sorted(glob.glob(tmp_path+"*.png")):
    body = Image.open(filename)
    signature = Image.open(sign_path)
    signature = signature.convert("RGBA")
    body.paste(signature, position, signature)
    body.convert('RGB')
    body.save(output_path+filename[len(tmp_path):-4]+".pdf", 'PDF',
              resolution=100.0, save_all=True,  quality=100)


clearFolder(input_path)
clearFolder(tmp_path)
os.rmdir(tmp_path)
