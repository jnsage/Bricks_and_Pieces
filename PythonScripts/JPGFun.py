# Resize all files in JPGs folder to be max size for Tableau
import os
import requests
from PIL import Image
from pathlib import Path

# Define the JPG Path
def jpg_path():
   cwd = Path.cwd().absolute()
   csv_folder = Path('JPGs')
   path = Path.joinpath(cwd,csv_folder).absolute()
   return path


# Request images for a list of image file URLs and save them into a JPG directory
def write_image(list: list, path: Path):
    for item in list:
        img_data = requests.get(item).content
        head, sep, tail = item.partition('elements/')
        write_path = Path.joinpath(path,tail)
        with open(write_path, 'wb') as handler:
            handler.write(img_data)


# Resize all files in JPGs folder to be max size for Tableau
def resize_files(directory: str):
    for filename in os.scandir(directory):
        if filename.is_file():
            im = Image.open(filename.path)
            im = im.resize((32, 32))
            im.save(filename.path)
            

if __name__ == "__main__":
    main()      
