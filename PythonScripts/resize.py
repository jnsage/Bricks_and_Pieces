# Resize all files in JPGs folder to be max size for Tableau
import os
import requests
from PIL import Image

# Request images for a list of image file URLs and save them into a JPG directory
def write_image(list: list):
    for item in list:
        img_data = requests.get(item).content
        head, sep, tail = item.partition('elements/')
        with open(f'./JPGs/{tail}', 'wb') as handler:
            handler.write(img_data)

# Resize all files in JPGs folder to be max size for Tableau
def resize_files(directory: str):
    for filename in os.scandir(directory):
        if filename.is_file():
            im = Image.open(filename.path)
            im = im.resize((32, 32))
            im.save(filename.path)
            

