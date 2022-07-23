# Resize all files in JPGs folder to be max size for Tableau
import os
import requests
from PIL import Image
from pathlib import Path
import pandas as pd

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

def make_list():
    top_ten_df = pd.read_csv('top_ten_parts.csv')
    part_num_list =[]
    part_color_list = []

    for item in top_ten_df['part_num']:
        part_num_list.append(item)
    for item in top_ten_df['color_id']:
        part_color_list.append(str(item))

    # Zip to tuple to lock in for API calls
    num_color_zip = zip(part_num_list,part_color_list)

    url_list = []
    for num, color in num_color_zip:
        response = requests.get(f'https://rebrickable.com/api/v3/lego/parts/{num}/colors/{color}?key={KEY_ONE}')
        data = response.json()
        url_list.append(str(data['part_img_url']))
    return url_list    


def main():
    make_list()
    path = jpg_path()
    write_image(url_list, path)     

if __name__ == "__main__":
    main()      
