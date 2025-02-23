# Adaptar para realizar con dirección ycambiar todos los tipos de archivos a uno mismo: jpg
from PIL import Image
import glob
ext = input('Input the original file extension: ')
new = input('Input the new file extension: ')


# Checks to see if a dot has been input with the images extensions.
# If not, it adds it for us:
if '.' not in ext.strip():
    ext = '.'+ext.strip()
if '.' not in new.strip():
    new = '.'+new.strip()

# Creates a list of all the files with the given extension in the current folder:
files = glob.glob('*'+ext)

# Converts the images:
for f in files:
    im = Image.open(f)
    im.save(f.replace(ext,new))
